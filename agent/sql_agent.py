from langchain.prompts import PromptTemplate
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.llms import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from db.connection import engine
from config.settings import OPENAI_API_KEY
import json
import logging
import traceback
from sqlalchemy import text

# 로깅 설정
logger = logging.getLogger(__name__)

def execute_sql_query(query: str) -> dict:
    """
    사용자 질문을 기반으로 직접 SQL을 실행하고 결과를 반환
    """
    try:
        # 사용자 질문을 기반으로 SQL 생성
        sql_query = generate_sql_from_query(query)
        logger.info(f"생성된 SQL: {sql_query}")
        
        # 직접 SQL 실행
        result = execute_direct_sql(sql_query)
        
        return {
            "success": True,
            "query": query,
            "result": result,
            "message": "쿼리가 성공적으로 실행되었습니다."
        }
        
    except Exception as e:
        logger.error(f"SQL 쿼리 실행 오류: {str(e)}")
        
        return {
            "success": False,
            "query": query,
            "error": str(e),
            "message": "쿼리 실행 중 오류가 발생했습니다."
        }

def generate_sql_from_query(user_query: str) -> str:
    """
    사용자 질문을 기반으로 SQL 쿼리를 생성
    """
    query_lower = user_query.lower()
    
    # 기본 SQL 쿼리 (모든 필드 포함)
    base_sql = """
    SELECT 
        id as product_id,
        product_name,
        description,
        thumbnail_image_url,
        price,
        discount_price,
        country_id,
        seller_id
    FROM product
    """
    
    # 키워드에 따른 WHERE 조건 추가
    if "테스트" in query_lower:
        return base_sql + " WHERE product_name LIKE '%테스트%' LIMIT 10"
    elif "제주" in query_lower:
        return base_sql + " WHERE product_name LIKE '%제주%' OR description LIKE '%제주%' LIMIT 10"
    elif "부산" in query_lower:
        return base_sql + " WHERE product_name LIKE '%부산%' OR description LIKE '%부산%' LIMIT 10"
    elif "가격" in query_lower or "price" in query_lower:
        return base_sql + " ORDER BY price ASC LIMIT 10"
    else:
        return base_sql + " LIMIT 10"

def execute_direct_sql(sql_query: str) -> str:
    """
    직접 SQL 쿼리를 실행하고 결과를 반환
    """
    try:
        logger.info(f"SQL 실행: {sql_query}")
        
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            rows = result.fetchall()
            
            if not rows:
                return "데이터를 찾을 수 없습니다."
            
            # 결과를 테이블 형태로 포맷팅
            formatted_result = []
            for row in rows:
                formatted_result.append(" | ".join(str(cell) for cell in row))
            
            return "\n".join(formatted_result)
            
    except Exception as e:
        logger.error(f"SQL 실행 오류: {str(e)}")
        raise e