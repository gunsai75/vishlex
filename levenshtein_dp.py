import gensim.downloader as api
import numpy as np
from nltk.metrics import edit_distance
from sklearn.metrics.pairwise import cosine_similarity

# Levenshtein distance but clubbed with the ability to consider word embeddings
# Used a dp table for optimisation

# Load a pre-trained word2vec model
word2vec_model = api.load("word2vec-google-news-300")

def get_word_embedding(word):
    """Get the word embedding for a word using Word2Vec."""
    try:
        return word2vec_model[word]
    except KeyError:
        # Return a vector of zeros if the word is not in the model's vocabulary
        return np.zeros(300)

def semantic_similarity(word1, word2):
    """Compute the semantic similarity between two words using cosine similarity."""
    vec1 = get_word_embedding(word1)
    vec2 = get_word_embedding(word2)
    
    return cosine_similarity([vec1], [vec2])[0][0]

def normalized_levenshtein_with_embeddings(str1, str2):
    """Calculate a normalized Levenshtein distance with semantic similarity using word embeddings."""
    # Tokenize the strings into words
    tokens1 = str1.split()
    tokens2 = str2.split()
    
    # Initialize an empty matrix to store distances
    n = len(tokens1)
    m = len(tokens2)
    dp = np.zeros((n + 1, m + 1))
    
    # Initialize base cases (edit distance for an empty string)
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    
    # Fill the DP table with Levenshtein distances
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            word1 = tokens1[i - 1]
            word2 = tokens2[j - 1]
            
            # Levenshtein distance calculations with semantic cost
            substitution_cost = 1 if word1 != word2 else 0
            if word1 != word2:
                # Use semantic similarity to adjust substitution cost
                semantic_sim = semantic_similarity(word1, word2)
                # Penalize less for semantically similar words
                substitution_cost = 1 - semantic_sim  # Higher similarity, lower cost
            
            # Choose the minimum cost operation (insertion, deletion, or substitution)
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # Deletion
                dp[i][j - 1] + 1,  # Insertion
                dp[i - 1][j - 1] + substitution_cost  # Substitution (including semantic cost)
            )
    
    # Normalize the final distance
    max_possible_distance = max(n, m)
    normalized_distance = dp[n][m] / max_possible_distance
    
    # Return a similarity score between 0 and 1 (1 means identical, 0 means entirely different)
    return 1 - normalized_distance


# TEST Example usage
# str1 = "The cat sat comfortably on the windowsill, basking in the warm sunlight."
# str2 = "The cat lounged on the window ledge, enjoying the warmth of the sun."

# distance = semantic_similarity(str1, str2)
# print(f"Levenshtein Distance with Semantic Similarity: {distance}")
