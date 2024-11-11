from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sacrebleu
from rouge_score import rouge_scorer
from nltk.translate.meteor_score import meteor_score
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
import levenshtein_dp
import deepl
import bert

DEEPL_API_KEY = r""

def fetch_translation(sourceText, targetLang):
    """Fetch translation using DeepL API."""
    translator = deepl.Translator(DEEPL_API_KEY)
    result = translator.translate_text(sourceText, target_lang=targetLang).text
    return result.lower()

def calculate_cosine_similarity(text1, text2):
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform both texts
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Calculate cosine similarity between the two vectors
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    # Return the similarity score
    return cosine_sim[0][0]

# def bleu_score(text1, text2):
#     score_bleu = sacrebleu.corpus_bleu([text2], [[text1]]).score
#     return score_bleu

# BLEU score
def bleu_score(text1, text2):
    reference = text1.split()
    candidate = text2.split()
    smoothie = SmoothingFunction().method4

    score_bleu = sentence_bleu([reference], candidate, smoothing_function=smoothie)
    return score_bleu

def calculate_rouge_score(ref, hyp):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(ref, hyp)
    f1m = scores['rougeL'].fmeasure # RougeL's fmeasure score for more a comprehensive score of similarity
    return f1m

def calculate_meteor_score(ref, hyp):
    ref_tokens = ref.split()
    hyp_tokens = hyp.split()

    score = meteor_score([ref_tokens], hyp_tokens)
    return score

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
    l_A_B_prime = levenshtein_dp.levenshtein_with_embeddings(A, B_prime)
    l_B_A_prime = levenshtein_dp.levenshtein_with_embeddings(B, A_prime)

    # BERT score
    b_A_B_prime = bert.bert_similarity(A, B_prime)
    b_B_A_prime = bert.bert_similarity(B, A_prime)

    scores = {
        "cosine_similarity": (cosine_A_B_prime + cosine_B_A_prime) / 2,
        "rouge_score": (rouge_A_B_prime + rouge_B_A_prime) / 2,
        "bleu_score": (bleu_A_B_prime + b_B_A_prime) / 2,
        "meteor_score": (met_A_B_prime + met_B_A_prime) / 2,
        "levenshtein_score": (l_A_B_prime + l_B_A_prime) / 2,
        "bert_score": (b_A_B_prime + b_B_A_prime) / 2
        # "levenshtein_similarity": (lev_dist_A_B_prime + lev_dist_B_A_prime) / 2,
        # "embedding_similarity": (embedding_similarity_A_B_prime + embedding_similarity_B_A_prime) / 2
    }
    scores["aggregate_quality_score"] = sum(scores.values()) / len(scores)

    return scores

