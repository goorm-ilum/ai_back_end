from sqlalchemy import create_engine
from config.settings import DB_URL
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

try:
    if not DB_URL:
        raise ValueError("DB_URL이 설정되지 않았습니다.")
    
    engine = create_engine(DB_URL, echo=True)
    
except Exception as e:
    logger.error(f"데이터베이스 연결 오류: {str(e)}")
    raise e