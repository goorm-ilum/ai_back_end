# 🤖 AI Backend Services

여행 상품 판매 플랫폼을 위한 AI 기반 백엔드 서비스입니다.

## ✨ 기능

### 🔍 SQL Database Agent
- 🗣️ 사용자 자연어 질문을 SQL로 변환
- 🔍 여행 상품 데이터베이스 조회
- 🔗 Spring Boot 프론트엔드와 연동하여 상품 ID 반환

### 📊 Review AI Analysis Service
- 🤖 KoELECTRA 기반 리뷰 감정 분석
- 📝 문장 단위 Aspect & Polarity 분류
- 🔄 Kafka를 통한 실시간 리뷰 데이터 처리
- 💾 MongoDB에 분석 결과 저장

## 🚀 설치 및 실행

### 1️⃣ 가상환경 생성 및 활성화

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2️⃣ 의존성 설치
```bash
pip install -r requirements.txt
```

### 3️⃣ 환경 변수 설정
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# MySQL Database
MYSQLDB_URL=mysql+pymysql://username:password@localhost:3306/database_name

# MongoDB
MONGODB_URL=mongodb://localhost:27017

# Kafka (선택사항)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092,localhost:9093,localhost:9094
KAFKA_TOPIC=review.raw
KAFKA_GROUP_ID=review-consumer-group
```

### 4️⃣ 서버 실행

**개발 환경:**
```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Docker 환경:**
```bash
# Docker 이미지 빌드
docker build -t ai-backend .

# Docker 컨테이너 실행
docker run -p 8000:8000 --env-file .env ai-backend
```

서버가 성공적으로 실행되면 `http://localhost:8000`에서 접근할 수 있습니다.

## 📡 API 엔드포인트

### 🔍 SQL Database Agent

#### POST /api/query
사용자 질문을 받아서 관련 여행 상품의 ID 목록을 반환합니다.

**Request:**
```json
{
  "query": "제주도 여행 상품 알려줘"
}
```

**Success Response:**
```json
{
  "product_ids": ["1", "3", "7"]
}
```

**No Results Response:**
```json
{
  "product_ids": []
}
```

**Error Response:**
```json
{
  "error": "오류 메시지"
}
```

### 📊 Review AI Analysis Service

#### Kafka Consumer (자동 처리)
- **Topic**: `review.raw`
- **처리 방식**: 실시간 스트리밍
- **출력**: MongoDB `review_keywords` 컬렉션에 저장

**Kafka 메시지 형식:**
```json
{
  "reviewId": "review_123",
  "productId": "product_456",
  "comment": "여행이 정말 좋았어요! 가이드도 친절하고..."
}
```

**MongoDB 저장 형식:**
```json
{
  "reviewId": "review_123",
  "productId": "product_456",
  "sentence": "여행이 정말 좋았어요!",
  "aspect": "service",
  "polarity": "positive"
}
```

## 💬 예시 질문

- 🏝️ "제주도 여행 상품 알려줘"
- 💰 "가격이 30만원 이하인 여행 상품"
- 🌊 "부산 해운대 여행 패키지"
- ⭐ "리뷰 평점이 높은 여행 상품"
- 🎉 "할인 중인 여행 상품"

## 🛠️ 개발 환경

### 🔧 주요 기술 스택

#### SQL Database Agent
- **FastAPI**: Python 웹 프레임워크
- **LangChain**: LLM 체인 구현
- **LangChain Experimental**: SQLDatabaseChain
- **OpenAI GPT**: 자연어를 SQL로 변환
- **SQLAlchemy**: 데이터베이스 ORM
- **PyMySQL**: MySQL 데이터베이스 연결

#### Review AI Analysis Service
- **KoELECTRA**: 한국어 전용 BERT 모델
- **Transformers**: Hugging Face 모델 라이브러리
- **PyTorch**: 딥러닝 프레임워크
- **Kafka**: 실시간 데이터 스트리밍
- **MongoDB**: 분석 결과 저장
- **Motor**: 비동기 MongoDB 드라이버

### 📋 필수 요구사항
- Python 3.11+
- MySQL 데이터베이스
- MongoDB
- Kafka (선택사항)
- OpenAI API 키

## ⚙️ 추가 설정

### 🧪 API 테스트
서버 실행 후 FastAPI 자동 문서를 통해 API를 테스트할 수 있습니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 📝 로그 확인
애플리케이션 실행 시 콘솔에서 다음과 같은 로그를 확인할 수 있습니다:
- `[SQL Agent]`: SQL Agent 처리 과정
- `[FastAPI]`: API 요청/응답 로그
- `[MongoDB]`: MongoDB 연결 및 저장 로그
- `[Kafka]`: Kafka 메시지 처리 로그
- `[Inference]`: AI 모델 추론 결과 로그

## 📁 프로젝트 구조

```
ai_back_end/
├── app/                           # 메인 애플리케이션
│   ├── main.py                   # FastAPI 앱 진입점
│   ├── routes/
│   │   └── products.py           # 상품 쿼리 처리 라우터
│   ├── agent/
│   │   └── sql_agent.py          # SQL Database Agent 구현
│   ├── services/
│   │   ├── ai_model.py           # AI 모델 추론 서비스
│   │   ├── predict.py            # KoELECTRA 예측 모델
│   │   └── preprocess.py         # 텍스트 전처리
│   ├── models/
│   │   ├── model.py              # KoELECTRA 모델 정의
│   │   ├── best_model.pt         # 학습된 모델 가중치
│   │   ├── aspect_encoder.pkl    # Aspect 라벨 인코더
│   │   └── polarity_mapping.pkl  # Polarity 라벨 매핑
│   ├── db/
│   │   ├── mysql.py              # MySQL 연결
│   │   └── mongo.py              # MongoDB 연결
│   ├── config/
│   │   ├── settings.py           # 환경변수 설정
│   │   └── kafka.py              # Kafka 설정
│   └── requirements.txt          # 의존성 목록
├── reviewmodel/                  # 리뷰 분석 모델 개발
│   ├── dataset/                  # 학습 데이터셋
│   ├── preprocessing.ipynb       # 데이터 전처리 노트북
│   └── new_preprocessing.ipynb   # 새로운 전처리 노트북
├── Dockerfile                    # Docker 컨테이너 설정
└── .env                         # 환경변수 파일 (생성 필요)
```