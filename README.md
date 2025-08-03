# AI SQL Agent Backend

여행 상품 판매 플랫폼을 위한 LLM 기반 SQL Agent 서버입니다.

## 기능

- 사용자 자연어 질문을 SQL로 변환
- 여행 상품 데이터베이스 조회
- Spring Boot와 연동하여 상품 정보 반환

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
OPENAI_API_KEY=your_openai_api_key_here
DB_URL=mysql+pymysql://username:password@localhost:3306/database_name
```

### 3. 서버 실행
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API 엔드포인트

### POST /api/query
사용자 질문을 받아서 여행 상품 정보를 반환합니다.

**Request:**
```json
{
  "query": "제주도 여행 상품 알려줘"
}
```

**Response:**
```json
[
  {
    "productId": 1,
    "productName": "제주도 3박4일 패키지",
    "productDescription": "제주도의 아름다운 자연을 만끽할 수 있는 패키지",
    "thumbnailImageUrl": "https://example.com/jeju.jpg",
    "price": 300000,
    "discountPrice": 250000,
    "averageReviewStar": 4.7,
    "isLiked": false
  }
]
```

## 예시 질문

- "제주도 여행 상품 알려줘"
- "가격이 30만원 이하인 여행 상품"
- "부산 해운대 여행 패키지"
- "리뷰 평점이 높은 여행 상품"
- "할인 중인 여행 상품"

## 프로젝트 구조

```
ai_back_end/
├── main.py                 # FastAPI 앱 진입점
├── routes/
│   └── query.py           # 쿼리 처리 라우터
├── agent/
│   └── sql_agent.py       # SQL Agent 구현
├── models/
│   └── product_response.py # 응답 모델
├── db/
│   └── connection.py      # 데이터베이스 연결
├── config/
│   └── settings.py        # 설정 관리
└── requirements.txt       # 의존성 목록
```