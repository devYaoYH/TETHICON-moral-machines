// public/js/main.js
document.addEventListener('DOMContentLoaded', function() {
  // Handle collection form submission
  const collectionForm = document.querySelector('.collection-form');
  
  if (collectionForm) {
    collectionForm.addEventListener('submit', function(event) {
      event.preventDefault();
      
      const collectionName = this.elements.collection.value.trim();
      
      if (collectionName) {
        window.location.href = `/?collection=${encodeURIComponent(collectionName)}`;
      }
    });
  }

  // Handle download CSV button click
  const downloadCsvBtn = document.getElementById('downloadCsv');
  if (downloadCsvBtn) {
    downloadCsvBtn.addEventListener('click', function() {
      const urlParams = new URLSearchParams(window.location.search);
      const collection = urlParams.get('collection') || 'TaskLogs';
      const executionId = urlParams.get('executionId') || 'age_expt_2';
      
      // Construct download URL
      const downloadUrl = `/download-csv?collection=${encodeURIComponent(collection)}&executionId=${encodeURIComponent(executionId)}`;
      
      // Trigger download
      window.location.href = downloadUrl;
    });
  }
});