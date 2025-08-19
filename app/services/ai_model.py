
def run_inference(review_data):
    
    # 2) 모델 출력 처리
    processed_result = {
        "reviewId": review_data["reviewId"],
        "productId": review_data["productId"],
        "sentiment": "positive"  # 실제 모델 출력 값으로 교체
    }
    
    # 3) Kafka에 넣기 위해 return
    return processed_result

if __name__ == "__main__":
    test_data = {"reviewId":11,"productId":1,"comment":"야호야호야호야호야호"}
    print(run_inference(test_data))