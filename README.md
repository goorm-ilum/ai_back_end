# 🤖 AI SQL Agent Backend

여행 상품 판매 플랫폼을 위한 LLM 기반 SQL Agent 서버입니다.

## ✨ 기능

- 🗣️ 사용자 자연어 질문을 SQL로 변환
- 🔍 여행 상품 데이터베이스 조회
- 🔗 Spring Boot 프론트엔드와 연동하여 상품 ID 반환

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
OPENAI_API_KEY=your_openai_api_key_here
MYSQLDB_URL=mysql+pymysql://username:password@localhost:3306/database_name
```

### 4️⃣ 서버 실행
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

서버가 성공적으로 실행되면 `http://localhost:8000`에서 접근할 수 있습니다.

## 📡 API 엔드포인트

### POST /api/query
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

## 💬 예시 질문

- 🏝️ "제주도 여행 상품 알려줘"
- 💰 "가격이 30만원 이하인 여행 상품"
- 🌊 "부산 해운대 여행 패키지"
- ⭐ "리뷰 평점이 높은 여행 상품"
- 🎉 "할인 중인 여행 상품"

## 🛠️ 개발 환경

### 🔧 주요 기술 스택
- **FastAPI**: Python 웹 프레임워크
- **LangChain**: LLM 체인 구현
- **OpenAI GPT**: 자연어를 SQL로 변환
- **SQLAlchemy**: 데이터베이스 ORM
- **PyMySQL**: MySQL 데이터베이스 연결

### 📋 필수 요구사항
- Python 3.7+
- MySQL 데이터베이스
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

## 📁 프로젝트 구조

```
ai_back_end/
├── main.py                 # FastAPI 앱 진입점
├── routes/
│   └── products.py        # 상품 쿼리 처리 라우터
├── agent/
│   └── sql_agent.py       # SQL Agent 구현
├── db/
│   └── connection.py      # 데이터베이스 연결
├── config/
│   └── settings.py        # 환경변수 및 설정 관리
├── requirements.txt       # 의존성 목록
└── .env                   # 환경변수 파일 (생성 필요)
``