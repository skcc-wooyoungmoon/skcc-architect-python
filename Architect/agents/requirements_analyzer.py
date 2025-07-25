# agents/requirements_analyzer.py
import os
from langchain_openai import AzureChatOpenAI

def analyze_requirements(state):
    """사용자의 요구사항을 분석하고 핵심 요소를 정리합니다."""
    user_input = state["user_input"]
    
    llm = AzureChatOpenAI(
        openai_api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        azure_deployment=os.getenv("AOAI_DEPLOY_GPT4O_MINI"), # 더 빠르고 저렴한 모델 사용
        openai_api_version=os.getenv("AOAI_API_VERSION"),
        temperature=0,
    )
    
    prompt = f"""
    [역할]
    당신은 뛰어난 시스템 분석가(System Analyst)입니다. 사용자가 제시한 시스템/서비스 요구사항을 분석하여 핵심 기능, 목표, 제약사항 등을 명확하게 구조화된 형태로 정리하는 역할을 맡고 있습니다.

    [지시사항]
    1. 아래에 주어진 [사용자 요구사항]을 면밀히 검토하세요.
    2. 요구사항을 다음 항목으로 분류하여 마크다운 형식으로 정리해주세요:
        - **핵심 기능 (Core Features):** 시스템이 반드시 제공해야 하는 주요 기능 목록
        - **주요 목표 (Key Objectives):** 이 시스템을 통해 달성하고자 하는 비즈니스 또는 기술적 목표
        - **사용자 및 규모 (Users & Scale):** 예상되는 주 사용자 그룹과 시스템이 처리해야 할 트래픽/데이터 규모
        - **성능/보안/기타 제약조건 (Constraints):** 성능 요구사항(응답시간 등), 데이터 민감도, 보안 수준, 기술 스택 제약 등 중요한 제약 조건
    3. 각 항목은 명확하고 간결한 문장으로 요약하여 제시해야 합니다.

    [사용자 요구사항]
    {user_input}
    """
    
    response = llm.invoke(prompt)
    print("--- 요구사항 분석 완료 ---")
    return response.content