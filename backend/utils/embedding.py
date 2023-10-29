from transformers import AutoTokenizer, AutoModel
import torch
from utils.milvus import Milvus

embeddings = []

def generate_primary_embedding(sentence):
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModel.from_pretrained("bert-base-uncased")

    # Tokenize and obtain the sentence embedding
    inputs = tokenizer(sentence, return_tensors="pt", padding=False, truncation=True) # pt - PyTorch, tf - Tensorflow, np - Numpy
    outputs = model(**inputs)
    sentence_vector = torch.mean(outputs.last_hidden_state, dim=1)
    embeddings.append(sentence_vector)

    a = Milvus()
    a.store_embeddings(sentence_vector)

    return sentence_vector

def get_embedding():
    return embeddings

# clear the embeddings list at the end of the week
def clear_embedding():
    embeddings = []
    return None
