from transformers import AutoTokenizer, AutoModel
import torch

embeddings = []

def generate_primary_embedding(sentence, takeAverage=False):
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModel.from_pretrained("bert-base-uncased")

    # Tokenize and obtain the sentence embedding
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True) # pt - PyTorch, tf - Tensorflow, np - Numpy
    outputs = model(**inputs)
    if takeAverage:
        sentence_vector = torch.mean(outputs.last_hidden_state, dim=1)
        embeddings.append(sentence_vector)
        return sentence_vector
    else:
        embeddings.append(outputs.last_hidden_state)
        return outputs.last_hidden_state

def get_embedding():
    return embeddings