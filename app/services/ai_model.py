from app.services.predict import predict
from app.services.preprocess import split_and_merge_sentences

def run_inference(review_data):
    review_comment = review_data["comment"]

    # --- 전처리: 문장 분리 + 병합 ---
    sentences = split_and_merge_sentences(review_comment)

    results = []
    for sentence in sentences:
        aspect_label, polarity_label = predict(sentence)
        results.append({
            "reviewId": review_data["reviewId"],
            "productId": review_data["productId"],
            "sentence": sentence,
            "aspect": aspect_label,
            "polarity": polarity_label
        })

    return results
