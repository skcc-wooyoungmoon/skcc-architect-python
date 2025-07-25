# langgraph_flow.py
from typing import TypedDict, Annotated
from typing_extensions import Literal
from langgraph.graph import StateGraph, END

# 에이전트 함수들을 임포트합니다.
from agents.requirements_analyzer import analyze_requirements
from agents.architect import design_architecture
from agents.security_expert import review_security
from agents.cost_optimizer import optimize_cost
from agents.devops_expert import suggest_devops
from agents.summarizer import summarize_all

# LangGraph의 상태를 정의하는 클래스
# 각 에이전트의 작업 결과가 여기에 저장됩니다.
class AgentState(TypedDict):
    user_input: str
    analysis_result: str
    design_result: str
    security_result: str
    cost_result: str
    devops_result: str
    summary_final_result: str

def build_architecture_flow():
    """아키텍처 설계 및 검토를 위한 LangGraph 워크플로우를 구축합니다."""
    graph = StateGraph(AgentState)

    # 1. 요구사항 분석 노드
    def run_analyze_requirements(state: AgentState) -> dict:
        result = analyze_requirements(state)
        return {"analysis_result": result}

    # 2. 아키텍처 설계 노드
    def run_design_architecture(state: AgentState) -> dict:
        result = design_architecture(state)
        return {"design_result": result}
    
    # 3. 보안 검토 노드
    def run_review_security(state: AgentState) -> dict:
        result = review_security(state)
        return {"security_result": result}

    # 4. 비용 최적화 노드
    def run_optimize_cost(state: AgentState) -> dict:
        result = optimize_cost(state)
        return {"cost_result": result}

    # 5. DevOps 전략 노드
    def run_suggest_devops(state: AgentState) -> dict:
        result = suggest_devops(state)
        return {"devops_result": result}

    # 6. 최종 요약 노드
    def run_summarize_all(state: AgentState) -> dict:
        result = summarize_all(state)
        return {"summary_final_result": result}


    # 워크플로우의 각 노드를 추가합니다.
    graph.add_node("analyze", run_analyze_requirements)
    graph.add_node("design", run_design_architecture)
    graph.add_node("security", run_review_security)
    graph.add_node("cost", run_optimize_cost)
    graph.add_node("devops", run_suggest_devops)
    graph.add_node("summarize", run_summarize_all)
    
    # 그래프의 시작점을 명시적으로 설정합니다.
    graph.set_entry_point("analyze")

    # 노드 간의 엣지(연결)를 순차적으로 정의합니다.
    graph.add_edge("analyze", "design")
    graph.add_edge("design", "security")
    graph.add_edge("security", "cost")
    graph.add_edge("cost", "devops")
    graph.add_edge("devops", "summarize")

    # 모든 작업이 완료되면 "summarize" 노드를 거쳐 종료(END)합니다.
    graph.add_edge("summarize", END)

    # 정의된 그래프를 컴파일하여 실행 가능한 애플리케이션으로 만듭니다.
    return graph.compile()