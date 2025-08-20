from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import MYSQLDB_URL

# 동기식 엔진 생성
engine = create_engine(MYSQLDB_URL, echo=True)

# 세션 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 세션 가져오기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
