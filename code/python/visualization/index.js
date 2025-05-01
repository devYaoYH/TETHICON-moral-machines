// index.js - Main application file (IAM authentication only)
const express = require('express');
const { Firestore } = require('@google-cloud/firestore');
const path = require('path');
const { Parser } = require('json2csv');

const app = express();
const port = process.env.PORT || 8080;

// Initialize Firestore
const firestore = new Firestore();

// Serve static files
app.use(express.static('public'));

// Set up template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Route to display documents
app.get('/', async (req, res) => {
  try {
    // Get collection name from query parameter or use default
    const collectionName = req.query.collection || 'TaskLogs';
    const executionId = req.query.executionId || 'age_expt_2';
    
    // Query all documents in the collection
    const snapshot = await firestore.collection(collectionName).get();
    
    // Convert data to a format easier to work with in the template
    const documents = [];
    snapshot.forEach(doc => {
      documents.push({
        id: doc.id,
        data: doc.data()
      });
    });

    // Get the superset of all document data headers
    const headers = new Set();
    documents.forEach(doc => {
      Object.keys(doc.data).forEach(key => headers.add(key));
    });
    
    // Get user info from headers (if available)
    const userEmail = req.headers['x-goog-authenticated-user-email'] 
      ? req.headers['x-goog-authenticated-user-email'].split(':').pop() 
      : 'Authenticated User';
    
    // Render the template with data
    res.render('index', { 
      headers: Array.from(headers),
      documents: documents,
      collectionName: collectionName,
      executionId: executionId,
      userEmail: userEmail
    });
  } catch (error) {
    console.error('Error fetching documents:', error);
    res.status(500).render('error', { error: error.message });
  }
});

// Route to download documents as CSV
app.get('/download-csv', async (req, res) => {
  try {
    const collectionName = req.query.collection || 'TaskLogs';
    const executionId = req.query.executionId || 'age_expt_2';
    
    const snapshot = await firestore.collection(collectionName).get();
    const documents = [];
    
    snapshot.forEach(doc => {
      if (doc.data().execution_id === executionId) {
        // Flatten the document data
        const flatData = { id: doc.id, ...doc.data() };
        // Convert objects to JSON strings
        for (const [key, value] of Object.entries(flatData)) {
          if (typeof value === 'object' && value !== null) {
            flatData[key] = JSON.stringify(value);
          }
        }
        documents.push(flatData);
      }
    });

    if (documents.length === 0) {
      return res.status(404).send('No documents found');
    }

    // Create CSV parser with all fields
    const fields = Array.from(new Set(documents.flatMap(doc => Object.keys(doc))));
    const parser = new Parser({ fields });
    const csv = parser.parse(documents);

    // Set headers for file download
    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', `attachment; filename=${collectionName}-${executionId}.csv`);
    res.send(csv);

  } catch (error) {
    console.error('Error generating CSV:', error);
    res.status(500).send('Error generating CSV file');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
