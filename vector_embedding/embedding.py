from transformers import AutoTokenizer, AutoModel
import torch

def generate_primary_embedding(sentence):
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModel.from_pretrained("bert-base-uncased")

    # Tokenize and obtain the sentence embedding
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    sentence_vector = torch.mean(outputs.last_hidden_state, dim=1)
    return sentence_vector
