from fastapi import APIRouter
from pydantic import BaseModel
from agent.sql_agent import ask_sql_agent

router = APIRouter()

class AIProductQuery(BaseModel):
    query: str

@router.post("/query")
async def search_products_with_ai(request: AIProductQuery):
    try:
        raw_result = ask_sql_agent(request.query)
        id_list = [id.strip() for id in raw_result.split(",") if id.strip().isdigit()]
        
        return {"product_ids": id_list}
    
    except Exception as e:
        return {"error": str(e)}
