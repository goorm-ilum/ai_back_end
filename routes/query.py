from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from models.product_response import ProductSummaryResponse
from agent.sql_agent import execute_sql_query
import json
import re
import logging
import traceback

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query", response_model=List[ProductSummaryResponse])
async def process_query(request: QueryRequest):
    """
    사용자 질문을 받아서 SQL Agent로 처리하고 상품 정보를 반환
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="쿼리가 비어있습니다.")
        
        result = execute_sql_query(request.query)
        
        if not result["success"]:
            logger.error(f"SQL Agent 실행 실패: {result['message']}")
            raise HTTPException(status_code=500, detail=result["message"])
        
        products = parse_sql_result_to_products(result["result"])
        return products
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API 요청 처리 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"SQL Agent 처리 중 오류 발생: {str(e)}")

def parse_sql_result_to_products(sql_result: str) -> List[ProductSummaryResponse]:
    """
    SQL Agent 결과를 ProductSummaryResponse 형태로 변환
    """
    try:
        if "죄송합니다" in str(sql_result):
            raise ValueError("여행 상품과 관련 없는 질문입니다. 여행 상품에 대한 질문을 해주세요.")
        
        products = []
        
        # 직접 SQL 실행 결과 파싱 (| 구분자로 분리된 데이터)
        lines = str(sql_result).split('\n')
        
        for line in lines:
            line = line.strip()
            if line and '|' in line:
                product_data = parse_table_row(line)
                if product_data:
                    products.append(ProductSummaryResponse.from_dict(product_data))
        
        if not products:
            logger.error(f"DB 데이터 파싱 실패. SQL Agent 결과: {sql_result}")
            raise ValueError("데이터베이스에서 상품 정보를 찾을 수 없거나 파싱할 수 없습니다.")
        
        return products
        
    except Exception as e:
        logger.error(f"SQL 결과 파싱 오류: {str(e)}")
        raise e

def parse_table_row(row: str) -> dict:
    """
    테이블 행을 파싱하여 딕셔너리로 변환
    """
    try:
        parts = [part.strip() for part in row.split('|') if part.strip()]
        logger.info(f"파싱된 파트: {parts}")
        
        if len(parts) >= 8:  # 8개 필드: id, product_name, description, thumbnail_image_url, price, discount_price, country_id, seller_id
            return {
                'product_id': int(parts[0]),
                'product_name': parts[1],
                'description': parts[2],
                'thumbnail_image_url': parts[3],
                'price': int(parts[4]),
                'discount_price': int(parts[5]),
                'average_review_star': 0.0  # 기본값
            }
    except Exception as e:
        logger.error(f"테이블 행 파싱 오류: {str(e)}")
        pass
    return None
