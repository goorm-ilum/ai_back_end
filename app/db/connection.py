from sqlalchemy import create_engine
from app.config.settings import DB_URL

engine = create_engine(DB_URL)

def get_mysql_engine():
    return engine
