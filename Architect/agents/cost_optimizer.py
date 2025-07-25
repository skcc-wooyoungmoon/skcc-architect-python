# agents/cost_optimizer.py
import os
from langchain_openai import AzureChatOpenAI

def optimize_cost(state):
    """설계된 아키텍처의 비용 최적화 방안을 제안합니다."""
    analysis_result = state["analysis_result"]
    design_result = state["design_result"]

    llm = AzureChatOpenAI(
        openai_api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        azure_deployment=os.getenv("AOAI_DEPLOY_GPT4O"),
        openai_api_version=os.getenv("AOAI_API_VERSION"),
        temperature=0.2,
    )

    prompt = f"""
    [역할]
    당신은 FinOps 전문가(FinOps Specialist)입니다. 제시된 [아키텍처 설계안]을 분석하여 비용 효율적인 클라우드 운영을 위한 구체적인 최적화 방안을 제안하는 역할을 맡고 있습니다.

    [지시사항]
    1. [아키텍처 설계안]에 제시된 기술 스택과 구성 요소들의 비용 모델(예: On-demand, Reserved Instances, Spot, 서버리스 과금)을 고려하세요.
    2. 각 구성 요소별로 비용을 절감할 수 있는 방안을 제안하세요. (예: 적정 인스턴스 타입 선택, 스토리지 티어링, 서버리스 메모리 최적화, 오토스케일링 정책 등)
    3. [요구사항 분석 결과]에 언급된 예산 제약이 있다면, 이를 충족하기 위한 트레이드오프(성능 vs 비용)를 고려하여 제안하세요.
    4. 초기 구축 비용과 월별 예상 운영 비용을 대략적으로 추정하고, 그 근거를 설명해주세요.

    [요구사항 분석 결과]
    {analysis_result}

    [아키텍처 설계안]
    {design_result}

    [비용 최적화 방안]
    """

    response = llm.invoke(prompt)
    print("--- 비용 최적화 분석 완료 ---")
    return response.content