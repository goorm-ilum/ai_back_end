import os
import torch
import joblib
from transformers import AutoTokenizer
from app.models.model import KoELECTRAMultiTask

# --- 디바이스 설정 ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- BASE_DIR ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- 모델/토크나이저/인코더 1회 로딩 ---
tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")

aspect_encoder = joblib.load(os.path.join(BASE_DIR, "../models/aspect_encoder.pkl"))
polarity_mapping = joblib.load(os.path.join(BASE_DIR, "../models/polarity_mapping.pkl"))
inv_polarity_mapping = {v: k for k, v in polarity_mapping.items()}

num_aspect_classes = len(aspect_encoder.classes_)
num_polarity_classes = len(polarity_mapping)

model = KoELECTRAMultiTask(
    "monologg/koelectra-base-v3-discriminator",
    num_aspect_classes,
    num_polarity_classes
).to(device)

checkpoint = torch.load(os.path.join(BASE_DIR, "../models/best_model.pt"), map_location=device)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

# --- predict 함수 ---
def predict(review_comment):
    inputs = tokenizer(
        review_comment,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    with torch.no_grad():
        aspect_logits, polarity_logits = model(input_ids, attention_mask)
        aspect_pred = torch.argmax(aspect_logits, dim=1).cpu().item()
        polarity_pred = torch.argmax(polarity_logits, dim=1).cpu().item()

    aspect_label = aspect_encoder.inverse_transform([aspect_pred])[0]
    polarity_label = inv_polarity_mapping[polarity_pred]

    return aspect_label, polarity_label
