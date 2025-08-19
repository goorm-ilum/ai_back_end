import os
import torch
import joblib
from transformers import AutoTokenizer
from app.models.model import KoELECTRAMultiTask  # 절대 import

# --- inference 함수 정의 ---
def run_inference(review_comment):
    # --- 현재 파일 기준 절대 경로 설정 ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # --- 디바이스 설정 ---
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # --- 토크나이저 로드 ---
    tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")

    # --- 저장된 인코더 및 매핑 불러오기 ---
    aspect_encoder_path = os.path.join(BASE_DIR, "../models/aspect_encoder.pkl")
    polarity_mapping_path = os.path.join(BASE_DIR, "../models/polarity_mapping.pkl")
    model_path = os.path.join(BASE_DIR, "../models/best_model.pt")

    aspect_encoder = joblib.load(aspect_encoder_path)
    polarity_mapping = joblib.load(polarity_mapping_path)
    inv_polarity_mapping = {v: k for k, v in polarity_mapping.items()}

    # --- 모델 불러오기 ---
    num_aspect_classes = len(aspect_encoder.classes_)
    num_polarity_classes = len(polarity_mapping)

    model = KoELECTRAMultiTask(
        "monologg/koelectra-base-v3-discriminator",
        num_aspect_classes,
        num_polarity_classes
    ).to(device)

    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    # --- 입력 데이터 토크나이징 ---
    inputs = tokenizer(
        review_comment,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # --- 추론 ---
    with torch.no_grad():
        aspect_logits, polarity_logits = model(input_ids, attention_mask)
        aspect_pred = torch.argmax(aspect_logits, dim=1).cpu().item()
        polarity_pred = torch.argmax(polarity_logits, dim=1).cpu().item()

    # --- 레이블 역변환 ---
    aspect_label = aspect_encoder.inverse_transform([aspect_pred])[0]
    polarity_label = inv_polarity_mapping[polarity_pred]

    return aspect_label, polarity_label


# --- 테스트 실행 ---
if __name__ == "__main__":
    test_data = {"reviewId": 11, "productId": 1, "comment": "불친절한 서비스에 실망했습니다."}
    aspect, polarity = run_inference(test_data["comment"])
    print(f"Aspect: {aspect}, Polarity: {polarity}")
