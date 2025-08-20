from dotenv import load_dotenv
import os
import logging

# 로깅 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MYSQLDB_URL = os.getenv("MYSQLDB_URL")

if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY가 설정되지 않았습니다!")
else:
    logger.info("OPENAI_API_KEY 로드 완료")

if not MYSQLDB_URL:
    logger.error("MYSQLDB_URL이 설정되지 않았습니다!")
else:
    logger.info("MYSQLDB_URL 로드 완료")