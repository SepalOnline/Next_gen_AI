# predict.py
import os, sys, json

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pyvi import ViTokenizer

def predict(text):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "phobert_sentiment_model")
    
    device = torch.device('cpu')
    torch.set_num_threads(1)
    
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    model.eval()
    
    text_segmented = ViTokenizer.tokenize(text)
    encoded = tokenizer(text_segmented, padding='max_length', truncation=True,
                        max_length=128, return_tensors='pt').to(device)
    
    with torch.no_grad():
        logits = model(**encoded).logits
        probs = F.softmax(logits, dim=-1).cpu().numpy()[0]
    
    predicted = int(torch.argmax(logits, dim=-1).item())
    result = {
        "predicted": predicted,
        "probs": [float(probs[0]), float(probs[1]), float(probs[2])]
    }
    print(json.dumps(result))

if __name__ == "__main__":
    text = sys.argv[1]
    predict(text)