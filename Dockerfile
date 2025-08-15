# 1. Python 3.11 slim 이미지 사용
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 설치
COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# 4. 프로젝트 전체 복사
COPY app/ .

# 5. .env 파일은 이미지에 포함하지 않고, 실행 시 --env-file로 주입 권장
# COPY app/.env .env   # <- 보안 위해 제거

# 6. 컨테이너 실행 명령 (t2.small → workers 1)
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers", "1"]
