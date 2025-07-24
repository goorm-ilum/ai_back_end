from fastapi import APIRouter
from agent.sql_agent import get_sql_agent

router = APIRouter()
agent = get_sql_agent()

@router.post("/ask/")
async def ask_question(payload: dict):
    question = payload.get("question")
    if not question:
        return {"error": "질문을 입력해주세요."}

    try:
        response = agent.run(question)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}
