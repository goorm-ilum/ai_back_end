from langchain.prompts import PromptTemplate
from langchain.agents import create_sql_agent
from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from db.connection import engine
from config.settings import OPENAI_API_KEY

def get_sql_agent():
    db = SQLDatabase(engine)
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    table_info = db.get_table_info()

    custom_prompt = PromptTemplate(
    input_variables=["input", "table_info", "dialect"],
    template="""
    당신은 '여행 리뷰 커뮤니티'에서 작동하는 SQL 전문 AI입니다.
    당신의 임무는 사용자의 자연어 질문을 SQL로 변환하고, 그 결과를 한국어로 친절하게 요약하는 것입니다.

    ## 역할
    - 당신은 MySQL을 사용하는 여행 리뷰 데이터베이스의 SQL 전문가입니다.
    - 당신의 주요 목적은 사용자의 여행 관련 질문(여행지 추천, 후기, 일정, 분위기 등)에 적절한 SQL을 작성하는 것입니다.

    ## 데이터베이스 정보
    - 현재 테이블 정보: {table_info}
    - 데이터베이스 종류: {dialect}

    ## 규칙
    1. 사용자의 질문이 **여행과 관련된 경우에만** SQL 쿼리를 작성하세요.
    2. **여행과 관련 없는 질문**(예: 수학 문제, 시사, 뉴스 등)은 다음과 같이 답변하세요:
        → `"죄송합니다. 저는 여행 관련 정보만 안내할 수 있습니다."`
    3. SQL은 정확하게 작성하고, **LIMIT를 활용하여 결과 개수를 제한**하세요.
    4. SQL 쿼리를 작성한 후에는 **한국어로 요약된 설명**도 함께 제공합니다.

    ## 예시
    사용자 질문: “부산에 대한 리뷰 알려줘”
    → SQL: `SELECT * FROM reviews WHERE location LIKE '%부산%' LIMIT 5;`
    → 답변: “부산에 대한 최근 리뷰 5개를 알려드릴게요.”

    사용자 질문: “삼각함수 그래프 그려줘”
    → 답변: “죄송합니다. 저는 여행 관련 정보만 안내할 수 있습니다.”

    ## 사용자 질문:
    {input}
    """
    )

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        prompt=custom_prompt,  # 최신 버전에서 지원
        verbose=True
    )
    return agent_executor