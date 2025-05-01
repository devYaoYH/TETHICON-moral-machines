# Moral Machines Redux

How do LLMs reason about paired-choice moral tasks? The Moral Machine Experiment introduced a paired-choice preference task to examine the moral biases of human responders along a wide spectrum of attributes. These tasks involve selecting between two sets of dire consequences involving a runaway autonomous vehicle, either killing one group of characters or another. This research investigates the moral preferences of Large Language Models (LLMs) using a similar paradigm, focusing on choices involving Age (Younger vs. Older) and Species (Human vs. Pets). We examined whether LLMs exhibit similar biases as humans and if language-based prompting influences these preferences across Western (English), Southern (French), and Eastern (Japanese, Chinese) linguistic contexts. Two state-of-the-art LLM endpoints, Gemini 2.0 Flash and Claude 3.5 Haiku, were prompted with paired-choice scenarios designed to elicit their reasoning via Chain-of-Thought prompting. Our findings indicate that Claude 3.5 Haiku demonstrated alignment with some human preferences, significantly favoring saving younger over older characters and humans over pets. Furthermore, prompting Claude 3.5 Haiku with Eastern languages led to a decreased preference for saving younger individuals. Gemini 2.0 Flash significantly preferred saving humans over pets, but did not show a significant age-based preference. Southern language prompting did not significantly alter preferences for either model. Exploratory analysis revealed generally high consistency and coherence in LLM responses, although coherence was lower for Claude 3.5 Haiku in Japanese when considering species. This study highlights the nuanced and potentially culturally influenced ‘moral’ decision-making of LLMs. While LLMs may mirror some human preferences, they are not reliable substitutes for human subjects in social science research. We underscore the importance of examining consistency and coherence in LLM outputs and caution against the uncritical adoption of LLMs in studies of human morality. This work contributes a methodology for probing LLM reasoning in moral dilemmas and offers insights into their potential and limitations for social science research.

## Repository structure 

```
├── code
|   ├── python
│   └── R
├── data
└── papers
```

### code 

#### python

#### R 

### data 

Dataset collected during study:

### papers 

Paper draft location.

