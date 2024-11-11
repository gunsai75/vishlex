from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def get_sentence_embedding(sentence):
    """
    Get the BERT embedding for a sentence by using the [CLS] token's representation.
    
    Args:
    - sentence (str): Input sentence.

    Returns:
    - np.array: BERT embedding for the sentence.
    """
    # Tokenize and prepare input
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=128)
    
    # Pass input through BERT and get hidden states
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Take the embedding of the [CLS] token as the sentence embedding
    cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    return cls_embedding

def bert_similarity(sentence1, sentence2):
    """
    Calculate the cosine similarity between embeddings of two sentences.
    
    Args:
    - sentence1 (str): First sentence.
    - sentence2 (str): Second sentence.

    Returns:
    - float: Cosine similarity score between the two sentence embeddings.
    """
    emb1 = get_sentence_embedding(sentence1)
    emb2 = get_sentence_embedding(sentence2)
    return cosine_similarity([emb1], [emb2])[0][0]

# # Example sentences
# sentence1 = "She enjoys reading books on rainy afternoons."
# sentence2 = "She loves to read novels during rainy days."

# # Calculate similarity score
# similarity_score = bert_similarity(sentence1, sentence2)
# print(f"Cosine similarity between the sentences: {similarity_score}")
