import asyncio
from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.sql_agent import ask_sql_agent

router = APIRouter()

class AIProductQuery(BaseModel):
    query: str

@router.post("/query")
async def search_products_with_ai(request: AIProductQuery):
    try:
        print(f"[FastAPI] AI 검색 요청: {request.query}")
        
        # 실제 AI Agent 호출
        raw_result = await asyncio.to_thread(ask_sql_agent, request.query)
        print(f"[FastAPI] AI Agent 결과: {raw_result}")
        
        if "해당 상품은 존재하지 않습니다" in raw_result:
            print(f"[FastAPI] 검색 결과 없음: {raw_result}")
            return {"product_ids": []}
        
        #  상품 ID 추출
        id_list = [id.strip() for id in raw_result.split(",") if id.strip().isdigit()]
        print(f"[FastAPI] 추출된 상품 ID: {id_list}, 데이터타입: {type(id_list)}")
        
        return {"product_ids": id_list}
    
    except Exception as e:
        print(f"[FastAPI] 오류 발생: {str(e)}")
        return {"error": str(e)}

