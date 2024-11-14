from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rouge_score import rouge_scorer
from nltk.translate.meteor_score import meteor_score
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
import levenshtein_dp
import deepl
import bert

# Files for BERT (bert.py) and Levenshtein distance (levenshtein_dp.py) exist in the same directory 
# This file contains the code for translation, comparision, and evaluation

# API KEY
DEEPL_API_KEY = r""

# Function to fetch translation using DeepL API
def fetch_translation(sourceText, targetLang):
    """Fetch translation using DeepL API."""
    translator = deepl.Translator(DEEPL_API_KEY)
    result = translator.translate_text(sourceText, target_lang=targetLang).text
    return result.lower()

# Cosine Similarity 
def calculate_cosine_similarity(text1, text2):
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform both texts
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Calculate cosine similarity between the two vectors
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    # Return the similarity score
    return cosine_sim[0][0]

# BLEU score
def bleu_score(text1, text2):
    reference = text1.split()
    candidate = text2.split()
    smoothie = SmoothingFunction().method4

    score_bleu = sentence_bleu([reference], candidate, smoothing_function=smoothie)
    return score_bleu

# ROUGE score
def calculate_rouge_score(ref, hyp):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(ref, hyp)
    f1m = scores['rougeL'].fmeasure # RougeL's fmeasure score for more a comprehensive score of similarity
    return f1m

# METEOR score
def calculate_meteor_score(ref, hyp):
    ref_tokens = ref.split()
    hyp_tokens = hyp.split()

    score = meteor_score([ref_tokens], hyp_tokens)
    return score

# Calculating all the scores using this function
# We pass 4 parameters
"""
Source Text (A) --> Machine Translation (A')
Human Translation (B) --> Back Translation (B')

Source Translation (A) VS Back Translation (B')
Machine Translation (B) VS Human Translation (A')

Args:-
A - Source Text
B - Human Translation
A_prime - Machine Translation
B_prime - Back Translation (of the Human Translation)

Returns:-
dictionary: all the scores
"""

def calc_score(A, B, A_prime, B_prime):
    # Cosine Similarity
    cosine_A_B_prime = calculate_cosine_similarity(A, B_prime)
    cosine_B_A_prime = calculate_cosine_similarity(B, A_prime)
    
    # BLEU score
    bleu_A_B_prime = bleu_score(A, B_prime)
    bleu_B_A_prime = bleu_score(B, A_prime)

    # Rouge score
    rouge_A_B_prime = calculate_rouge_score(A, B_prime)
    rouge_B_A_prime = calculate_rouge_score(B, A_prime)

    # METEOR score
    met_A_B_prime = calculate_meteor_score(A, B_prime)
    met_B_A_prime = calculate_meteor_score(B, A_prime)

    # Levenshtein score
    l_A_B_prime = levenshtein_dp.normalized_levenshtein_with_embeddings(A, B_prime)
    l_B_A_prime = levenshtein_dp.normalized_levenshtein_with_embeddings(B, A_prime)

    # BERT score
    b_A_B_prime = bert.bert_similarity(A, B_prime)
    b_B_A_prime = bert.bert_similarity(B, A_prime)

    scores = {
        "Cosine Similarity": (cosine_A_B_prime + cosine_B_A_prime) / 2,
        "Rouge Score": (rouge_A_B_prime + rouge_B_A_prime) / 2,
        "BLEU Score": (bleu_A_B_prime + bleu_B_A_prime) / 2,
        "METEOR Score": (met_A_B_prime + met_B_A_prime) / 2,
        "Levenshtein Distance (normalized)": (l_A_B_prime + l_B_A_prime) / 2,
        "BERT Score": (b_A_B_prime + b_B_A_prime) / 2
    }
    scores["aggregate_quality_score"] = sum(scores.values()) / len(scores)

    return scores

