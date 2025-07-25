# agents/security_expert.py
import os
from langchain_openai import AzureChatOpenAI
from vector_db import search_docs

def review_security(state):
    """설계된 아키텍처에 대한 보안 취약점을 검토하고 개선 방안을 제안합니다."""
    analysis_result = state["analysis_result"]
    design_result = state["design_result"]
    
    # RAG: 설계안과 관련된 보안 체크리스트 검색
    rag_query = f"아키텍처 설계안: {design_result}\n 이 설계에 필요한 보안 고려사항은?"
    relevant_docs = search_docs(rag_query, top_k=2)
    
    rag_context = "\n\n".join([f"--- 참고자료: {doc['source']} ---\n{doc['content']}" for doc in relevant_docs])

    llm = AzureChatOpenAI(
        openai_api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        azure_deployment=os.getenv("AOAI_DEPLOY_GPT4O"),
        openai_api_version=os.getenv("AOAI_API_VERSION"),
        temperature=0.1,
    )
    
    prompt = f"""
    [역할]
    당신은 클라우드 보안 전문가(Cloud Security Specialist)입니다. 제시된 [요구사항 분석 결과]와 [아키텍처 설계안]을 바탕으로, 발생 가능한 보안 위협을 식별하고 이를 완화하기 위한 구체적인 보안 강화 방안을 제안하는 역할을 맡고 있습니다.

    [지시사항]
    1. [아키텍처 설계안]의 각 구성 요소(네트워크, 데이터, 애플리케이션, 접근 제어 등)를 분석하여 잠재적인 보안 취약점을 식별하세요.
    2. 식별된 위협에 대해, IAM 정책, 네트워크 보안(보안 그룹/VPC), 데이터 암호화, 로깅 및 모니터링 등 구체적인 해결책을 제시하세요.
    3. [요구사항 분석 결과]에 언급된 데이터 민감도나 규정 준수 요건이 있다면, 이를 충족하기 위한 추가적인 보안 조치를 제안하세요.
    4. 제공된 [참고 자료]를 활용하여 제안의 신뢰성을 높이세요.

    [요구사항 분석 결과]
    {analysis_result}

    [아키텍처 설계안]
    {design_result}

    [참고 자료]
    {rag_context if rag_context else "제공된 참고 자료 없음."}

    [보안 검토 및 제안]
    """
    
    response = llm.invoke(prompt)
    print("--- 보안 검토 완료 ---")
    return response.content