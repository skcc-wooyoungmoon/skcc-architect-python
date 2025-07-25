# agents/summarizer.py
import os
from langchain_openai import AzureChatOpenAI

def summarize_all(state):
    """모든 전문가의 의견을 종합하여 최종 요약 보고서를 작성합니다."""
    prompt = f"""
    [역할]
    당신은 프로젝트의 총괄 책임자인 수석 아키텍트(Chief Architect)입니다. 각 분야 전문가들의 분석 및 제안 내용을 하나의 일관된 최종 보고서로 종합하는 역할을 맡고 있습니다.

    [지시사항]
    1. 아래에 주어진 각 전문가의 의견([요구사항 분석], [아키텍처 설계], [보안 검토], [비용 최적화], [DevOps 전략])을 모두 검토하세요.
    2. 이 내용들을 바탕으로, 경영진이나 고객에게 보고할 수 있는 명확하고 설득력 있는 **최종 설계 가이드**를 작성해주세요.
    3. 최종 가이드는 다음 구조를 따라야 합니다:
        - **프로젝트 요약:** 사용자의 요구사항을 바탕으로 이 프로젝트가 무엇인지 한두 문단으로 요약합니다.
        - **핵심 아키텍처:** 제안된 아키텍처와 기술 스택의 핵심 내용을 요약합니다.
        - **주요 고려사항:** 보안, 비용, 운영 측면에서 반드시 고려해야 할 가장 중요한 3~5가지 포인트를 강조합니다.
        - **권장 실행 계획 (Action Plan):** 프로젝트를 성공적으로 진행하기 위한 다음 단계(예: PoC 개발, 상세 설계, 인프라 구축)를 간략하게 제안합니다.

    [요구사항 분석]
    {state.get('analysis_result', "분석 결과 없음")}

    [아키텍처 설계]
    {state.get('design_result', "설계안 없음")}

    [보안 검토]
    {state.get('security_result', "보안 검토 결과 없음")}

    [비용 최적화]
    {state.get('cost_result', "비용 최적화 방안 없음")}

    [DevOps 전략]
    {state.get('devops_result', "DevOps 전략 없음")}

    [최종 설계 가이드 요약]
    """
    llm = AzureChatOpenAI(
        openai_api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        azure_deployment=os.getenv("AOAI_DEPLOY_GPT4O"),
        openai_api_version=os.getenv("AOAI_API_VERSION"),
        temperature=0.2,
    )
    print("--- 최종 요약 보고서 생성 완료 ---")
    return llm.invoke(prompt).content