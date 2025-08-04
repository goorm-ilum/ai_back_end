from langchain_openai import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from config.settings import OPENAI_API_KEY
from db.connection import get_mysql_engine

def ask_sql_agent(query: str):
    engine = get_mysql_engine()
    db = SQLDatabase(engine=engine)
    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    prompt = f"""
    당신은 여행 상품 데이터베이스에서 SQL을 이용해 사용자의 질문에 적절한 여행 상품들을 찾는 AI입니다.

    # 지침:
    - 아래 사용자의 질문을 바탕으로 SQL을 작성하여 상품을 검색하세요.
    - 검색 결과로 얻은 **상품 ID들만**, **숫자만**, **콤마(,)로 구분된 한 줄 문자열로만 출력**하세요.
    - 상품 ID는 반드시 숫자여야 하며, **숫자가 아닌 값은 제외**하세요.
    - 적절한 상품이 데이터베이스에 없거나, 질문이 상품과 관련 없다고 판단되면 "해당 상품은 존재하지 않습니다." 혹은 "찾으시는 여행 상품에 대한 질문을 입력해주세요."라는 문구로 출력해주세요.
    - 상품 ID의 콤마(,) 나열, "해당 상품은 존재하지 않습니다." 또는 "찾으시는 여행 상품에 대한 질문을 입력해주세요." 문구 외에는 **어떠한 추가 설명도 하지 마세요**.
    - 그 외에는 **어떠한 설명도 출력하지 마세요**. (예: "상품은 다음과 같습니다", "ID 목록은..." 등은 절대 하지 마세요)

    # 사용자 질문:
    {query}
    """

    result = db_chain.run(prompt)
    return result