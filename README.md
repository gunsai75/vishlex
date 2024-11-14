# Vishlex - Translation Quality Evaluation

Requirements
 - Python 3.7+
 - Flask
 - DeepL API key
 - All the required libraries / modules are in `requirements.txt`

# Problem Statement
 Traditionally, translation assessment is done manually, which is time-consuming and often subjective. This project seeks to solve this by creating an automated tool that uses machine-generated translations and various NLP similarity metrics to evaluate human translations. The result is a reliable, scalable, and more impartial assessment of translation accuracy and effectiveness.
 
# Key Functionalities
 ### Machine Translation Generation
  - Create a machine translation of the source text.
  - Back-translate the human translation into the original language.
  ```mermaid
  graph TD;
    "Source Text (A)" --> "Machine Translation (B)";
    "Human Translation (A')" --> "Back Translation (B')"; 
  ```
 ### Text Comparison:
 - Compare the source text with the back-translation.
 - Compare the human translation with the machine translation of the source text.

 **Source Text (A)** is compared against **Back Translation (B')** </br>
 **Human Translation (A')** is compared against **Machine Translation (B)**
 
### Similarity Score Calculation:
 Using various NLP metrics
- Cosine Similarity
- BLEU
- ROUGE
- METEOR
- Levenshtein Distance

### Calculating the Aggregate Score
We calculated the aggregate score by taking the mean value of all the scores.

# Why the DeepL API?
DeepL is known for its accuracy and natural, human-like translations, especially for European languages, making it suitable for assessing nuanced translation quality.

DeepL’s advanced AI handles idioms, tone, and context better than many alternatives, providing translations that are closer to human interpretation.

# Running the Program
Run the below line in the terminal to install the required libraries:
```
pip install -r "requirements.txt"
```
To run the program type tge following in the terminal:
```
python main.py
```

------- WIP ---------
