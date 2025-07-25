# app.py

import streamlit as st
from langgraph_flow import build_architecture_flow, AgentState
import os
from dotenv import load_dotenv

# .env 파일 로드 (AOAI_API_KEY 등이 여기에 있어야 함)
load_dotenv()

st.set_page_config(page_title="AI 아키텍처 설계 가이드", layout="wide")
st.title("🧑‍💻 AI 아키텍처 설계 어시스턴트")
st.caption("LangGraph와 Azure OpenAI를 활용한 자동 설계 제안 시스템")

st.markdown("""
서비스/시스템 요구사항을 입력하면, 아키텍처/보안/비용/운영 전문가 AI가 협업하여 최적의 설계 가이드와 참고 자료를 제공합니다.
""")

# 초기화: 세션 상태에 필요한 변수들을 설정합니다.
if 'result' not in st.session_state:
    st.session_state.result = None
if 'user_input_processed' not in st.session_state:
    st.session_state.user_input_processed = ""


with st.sidebar:
    st.header("📝 입력 가이드")
    st.markdown("""
    다음과 같은 정보를 포함하여 시스템 또는 서비스 요구사항을 자세히 입력해주세요:

    - **핵심 기능:** 시스템이 제공해야 하는 주요 기능
    - **목표 사용자:** 예상 사용자 및 규모
    - **성능 요구사항:** 응답 시간, 처리량 등
    - **데이터 특성:** 데이터 종류, 양, 민감도
    - **보안 요구사항:** 필요한 보안 수준, 규정 준수
    - **예산 제약:** 있다면 대략적인 범위
    - **선호 기술 스택:** 특정 기술 선호도 (선택 사항)
    - **기타 제약 조건:**
    """)
    st.divider()
    st.info("API 키와 엔드포인트는 `.env` 파일에 설정되어 있어야 합니다.")


user_input = st.text_area("시스템/서비스 요구사항을 입력하세요:", height=200, key="user_input_area", placeholder="예시) 월 100만명이 사용하는 중고 거래 플랫폼을 만들고 싶습니다. 실시간 채팅 기능과 이미지 업로드 기능이 필수입니다. 개인정보 보호가 매우 중요합니다.")

if st.button("🚀 설계 가이드 생성", type="primary", use_container_width=True):
    if user_input and user_input.strip():
        st.session_state.user_input_processed = user_input
        with st.status("🤖 AI 전문가들이 아키텍처를 설계하고 검토 중입니다...", expanded=True) as status:
            try:
                status.write("1/6: 요구사항 분석 전문가가 투입되었습니다...")
                flow = build_architecture_flow()
                
                # AgentState에 맞게 초기 상태 설정
                initial_state = AgentState(
                    user_input=user_input,
                    analysis_result="",
                    design_result="",
                    security_result="",
                    cost_result="",
                    devops_result="",
                    summary_final_result=""
                )
                
                # LangGraph 플로우 실행
                # stream 대신 invoke를 사용하여 최종 결과만 받음
                st.session_state.result = flow.invoke(initial_state)

                # UI 업데이트는 아래 결과 표시 부분에서 처리
                status.update(label="✅ 설계 가이드가 완성되었습니다!", state="complete", expanded=False)

            except Exception as e:
                st.error(f"설계 가이드 생성 중 오류가 발생했습니다: {e}")
                st.exception(e)
                st.session_state.result = None
    else:
        st.warning("요구사항을 입력해주세요.")

# 결과가 세션 상태에 있을 경우 화면에 표시
if st.session_state.result:
    result_data = st.session_state.result

    tab_titles = ["요구사항 분석", "아키텍처 설계", "보안 검토", "비용 최적화", "DevOps/운영", "최종 요약"]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        st.subheader("1️⃣ 요구사항 분석 결과")
        st.markdown(result_data.get('analysis_result', "분석 결과를 찾을 수 없습니다."))

    with tabs[1]:
        st.subheader("2️⃣ 아키텍처 설계안")
        st.markdown(result_data.get('design_result', "설계안을 찾을 수 없습니다."))

    with tabs[2]:
        st.subheader("3️⃣ 보안 검토 및 제안")
        st.markdown(result_data.get('security_result', "보안 검토 결과를 찾을 수 없습니다."))

    with tabs[3]:
        st.subheader("4️⃣ 비용 최적화 방안")
        st.markdown(result_data.get('cost_result', "비용 최적화 방안을 찾을 수 없습니다."))

    with tabs[4]:
        st.subheader("5️⃣ DevOps/운영 전략")
        st.markdown(result_data.get('devops_result', "DevOps/운영 전략을 찾을 수 없습니다."))

    with tabs[5]:
        st.subheader("✅ 최종 설계 가이드 요약")
        st.markdown(result_data.get('summary_final_result', "최종 요약 정보를 찾을 수 없습니다."))

    st.divider()
    
    # 다운로드할 텍스트 데이터 생성
    full_report = f"""
# AI 아키텍처 설계 가이드

## 원본 요구사항
{st.session_state.user_input_processed}

---

## 1. 요구사항 분석 결과
{result_data.get('analysis_result', "N/A")}

---

## 2. 아키텍처 설계안
{result_data.get('design_result', "N/A")}

---

## 3. 보안 검토 및 제안
{result_data.get('security_result', "N/A")}

---

## 4. 비용 최적화 방안
{result_data.get('cost_result', "N/A")}

---

## 5. DevOps/운영 전략
{result_data.get('devops_result', "N/A")}

---

## 최종 설계 가이드 요약
{result_data.get('summary_final_result', "N/A")}
"""
    
    st.download_button(
        label="📥 전체 설계 가이드 다운로드 (.md)",
        data=full_report.encode('utf-8'),
        file_name="ai_architecture_guide.md",
        mime="text/markdown"
    )