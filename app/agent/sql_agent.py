from langchain_openai import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from config.settings import OPENAI_API_KEY
from db.connection import get_mysql_engine
import re

def ask_sql_agent(query: str):
    """SQLDatabaseChain을 사용하여 상품 ID만 반환하는 AI Agent"""
    
    try:
        print(f"[SQL Agent] 시작 - 쿼리: {query}")
        
        # 데이터베이스 연결
        engine = get_mysql_engine()
        db = SQLDatabase(engine=engine)
        llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
        db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

        # 상품 ID만 반환하도록 특별한 프롬프트 작성
        prompt = f"""
        당신은 여행 상품 데이터베이스에서 SQL을 이용해 사용자의 질문에 적절한 여행 상품들을 찾는 AI입니다.

        # 데이터베이스 스키마:
        - product 테이블: 상품 정보 (id, product_name, description, price, etc.)
        - hash_tag 테이블: 해시태그 정보 (product_id, hashtag) - 실제 테이블명은 hashtag일 수 있음
        - review 테이블: 리뷰 정보 (product_id, comment, review_star)
        - likes 테이블: 좋아요 정보 (member_id, product_id)
        - country 테이블: 국가 정보 (country테이블의 경우 enum 타입으로 KR, JP 등으로 id가 설정되어있고, name이 한국어로 된 국가명임)

        # 중요 지침:
        - 사용자의 질문을 바탕으로 적절한 SQL 쿼리를 작성하세요.
        - 만일 특정 도시나 국가에 대한 질문이 들어오면, 해당 도시의 소속 국가에 관련된 상품을 검색하세요.(국내라고 한다면 대한민국을 의미)
        - **마크다운 형식(```sql, ```)을 절대 사용하지 마세요.**
        - **SQL 쿼리를 직접 실행하고 결과만 반환하세요.**
        - 검색 결과로 얻은 **상품 ID들만**, **숫자만**, **콤마(,)로 구분된 한 줄 문자열로만 출력**하세요.
        - 상품 ID는 반드시 숫자여야 하며, **숫자가 아닌 값은 제외**하세요.
        - 적절한 상품이 데이터베이스에 없거나, 질문이 상품과 관련 없다고 판단되면 "해당 상품은 존재하지 않습니다."를 출력하세요.
        - 상품 ID의 콤마(,) 나열 또는 "해당 상품은 존재하지 않습니다." 문구 외에는 **어떠한 추가 설명도 하지 마세요**.
        - 자연어 설명이나 다른 텍스트는 절대 출력하지 마세요.
        - **SQL 쿼리 자체를 출력하지 마세요. 오직 실행 결과만 출력하세요.**
        - **테이블이 존재하지 않으면 product 테이블만 사용하여 검색하세요.**

        # 예시 출력 형식:
        - "1,3,5" (상품 ID가 1, 3, 5인 경우)
        - "해당 상품은 존재하지 않습니다." (검색 결과가 없는 경우)

        # 사용자 질문:
        {query}
        """

        print(f"[SQL Agent] 프롬프트 실행 중...")
        result = db_chain.run(prompt)
        print(f"[SQL Agent] 원본 결과: {result}")
        
        # 결과 정리
        result = result.strip()
        
        # "해당 상품은 존재하지 않습니다" 체크
        if "해당 상품은 존재하지 않습니다" in result:
            print(f"[SQL Agent] 검색 결과 없음")
            return "해당 상품은 존재하지 않습니다."
        
        # 숫자와 콤마만 추출
        product_ids = re.findall(r'\d+', result)
        
        if not product_ids:
            print(f"[SQL Agent] 상품 ID 추출 실패")
            return "해당 상품은 존재하지 않습니다."
        
        # 결과 반환 (콤마로 구분된 ID 문자열)
        result_string = ",".join(product_ids)
        print(f"[SQL Agent] 최종 결과: {result_string}")
        return result_string
        
    except Exception as e:
        print(f"[SQL Agent] 오류 발생: {str(e)}")
        return "해당 상품은 존재하지 않습니다."