# agents/architect.py
import os
from langchain_openai import AzureChatOpenAI
from vector_db import search_docs

def design_architecture(state):
    """분석된 요구사항과 RAG 검색 결과를 바탕으로 아키텍처를 설계합니다."""
    analysis_result = state["analysis_result"]
    user_input = state["user_input"]

    # RAG: 요구사항과 관련된 아키텍처 모범 사례 검색
    rag_query = f"요구사항: {user_input}\n분석 결과: {analysis_result}\n 이 시스템에 적합한 아키텍처 스타일과 기술 스택은?"
    relevant_docs = search_docs(rag_query, top_k=2)
    
    rag_context = "\n\n".join([f"--- 참고자료: {doc['source']} ---\n{doc['content']}" for doc in relevant_docs])

    llm = AzureChatOpenAI(
        openai_api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        azure_deployment=os.getenv("AOAI_DEPLOY_GPT4O"),
        openai_api_version=os.getenv("AOAI_API_VERSION"),
        temperature=0.3,
    )
    
    prompt = f"""
    [역할]
    당신은 20년 경력의 솔루션 아키텍트(Solution Architect)입니다. 시스템 분석가의 [요구사항 분석 결과]와 [참고 자료]를 바탕으로, 확장 가능하고 안정적인 시스템 아키텍처를 설계하는 임무를 맡았습니다.

    [지시사항]
    1. [요구사항 분석 결과]를 깊이 이해하고, 이를 충족시킬 수 있는 최적의 아키텍처 스타일(예: 모놀리식, 마이크로서비스, 서버리스)을 제안하고 그 이유를 설명하세요.
    2. 주요 기술 스택(프론트엔드, 백엔드, 데이터베이스, 인프라 등)을 구체적으로 추천하고, 각 기술을 선택한 근거를 제시하세요.
    3. 시스템의 핵심 구성 요소들을 설명하고, 이들 간의 데이터 흐름과 상호작용을 설명하는 간단한 아키텍처 다이어그램(텍스트 기반 또는 Mermaid.js 형식)을 제시하세요.
    4. 제공된 [참고 자료]가 있다면, 설계에 어떻게 반영되었는지 언급해주세요.

    [요구사항 분석 결과]
    {analysis_result}

    [참고 자료]
    {rag_context if rag_context else "제공된 참고 자료 없음."}

    [아키텍처 설계안]
    """
    
    response = llm.invoke(prompt)
    print("--- 아키텍처 설계 완료 ---")
    return response.content