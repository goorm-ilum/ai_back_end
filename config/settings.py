from dotenv import load_dotenv
import os
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_URL = os.getenv("DB_URL")

# 환경 변수 설정 상태 확인
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY가 설정되지 않았습니다!")
if not DB_URL:
    logger.error("DB_URL이 설정되지 않았습니다!")