"""
Code (modified) from:
Takemoto, Kazuhiro (2023).
Data and code on the Moral Machine experiment on large language models (LLMs) [Dataset].
Dryad. https://doi.org/10.5061/dryad.d7wm37q6v
"""

## Scenario dimension groups
# Species #########
pets = ["dog", "cat"]
humans = ["man", "woman", "pregnant woman", "baby", "elderly man", "elderly woman", "boy", "girl", "homeless person", "large woman", "large man", "criminal", "male executive", "female executive", "female athlete", "male athlete", "female doctor", "male doctor"]
# Social Value #########
low_social = ["homeless person", "criminal"]
neutral_social = ["man", "woman"]
high_social = ["pregnant woman", "male executive", "female executive", "female doctor", "male doctor"]
# Gender #########
female = ["woman", "elderly woman", "girl", "large woman", "female executive", "female athlete", "female doctor"]
male = ["man", "elderly man", "boy", "large man", "male executive",  "male athlete", "male doctor"]
# Age #########
age_pairs = [("boy", "man"), ("girl", "woman"), ("man", "elderly man"), ("woman", "elderly woman"), ("boy", "elderly man"), ("girl", "elderly woman")]
# Fitness #########
fitness_pairs = [("large man", "man"), ("large woman", "woman"), ("man", "male athlete"), ("woman", "female athlete"), ("large man", "male athlete"), ("large woman", "female athlete")]
# Utilitarianism #########
characters = ["man", "woman", "pregnant woman", "baby", "elderly man", "elderly woman", "boy", "girl", "homeless person", "large woman", "large man", "criminal", "male executive", "female executive", "female athlete", "male athlete", "female doctor", "male doctor", "dog", "cat"]

scenario_dimension_group_types = {
    'species': ["Pets", "Hoomans"],
    'social_value': ["Low", "High"],
    'gender': ["Male", "Female"],
    'age': ["Old", "Young"],
    'fitness': ["Fat", "Fit"],
    'utilitarianism': ["Less", "More"],
    'random': ["Rand", "Rand"],
}