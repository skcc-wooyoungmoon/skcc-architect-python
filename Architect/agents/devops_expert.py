# agents/devops_expert.py
import os
from langchain_openai import AzureChatOpenAI

def suggest_devops(state):
    """설계된 아키텍처에 대한 CI/CD, 모니터링 등 DevOps 전략을 제안합니다."""
    analysis_result = state["analysis_result"]
    design_result = state["design_result"]

    llm = AzureChatOpenAI(
        openai_api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        azure_deployment=os.getenv("AOAI_DEPLOY_GPT4O"),
        openai_api_version=os.getenv("AOAI_API_VERSION"),
        temperature=0.3,
    )

    prompt = f"""
    [역할]
    당신은 DevOps 엔지니어(DevOps Engineer)입니다. 제시된 [아키텍처 설계안]을 안정적이고 효율적으로 구축, 배포, 운영하기 위한 DevOps 전략을 수립하는 역할을 맡고 있습니다.

    [지시사항]
    1. **CI/CD 파이프라인:** 코드 통합, 빌드, 테스트, 배포를 자동화하기 위한 CI/CD 파이프라인 구성 방안을 제안하세요. (추천 도구: GitHub Actions, Jenkins, Azure DevOps 등)
    2. **IaC (Infrastructure as Code):** 인프라를 코드로 관리하기 위한 방안을 제안하세요. (추천 도구: Terraform, CloudFormation)
    3. **모니터링 및 로깅:** 시스템의 상태를 실시간으로 파악하고 문제 발생 시 신속하게 대응하기 위한 모니터링 및 로깅 전략을 제안하세요. (추천 도구: Prometheus/Grafana, Datadog, Azure Monitor)
    4. **배포 전략:** 무중단 배포를 위한 배포 전략(예: 블루/그린, 카나리)을 제안하세요.

    [요구사항 분석 결과]
    {analysis_result}

    [아키텍처 설계안]
    {design_result}

    [DevOps/운영 전략]
    """

    response = llm.invoke(prompt)
    print("--- DevOps 전략 제안 완료 ---")
    return response.content