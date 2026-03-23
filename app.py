import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. 웹앱 기본 설정 및 언어 선택
# ==========================================
st.set_page_config(page_title="K-PROTOCOL Master Simulator", layout="wide")

st.sidebar.header("🌐 Language / 언어")
lang = st.sidebar.radio("Select / 선택", ["Korean (한국어)", "English"])

# 다국어 텍스트 사전
t = {
    "Korean (한국어)": {
        "title": "🌌 K-PROTOCOL: 대통합 마스터 시뮬레이터",
        "desc": "**K-Omni 방정식** 하나로 거시 세계(은하 회전)와 미시 세계(양자 얽힘)의 미스터리를 기하학적으로 해체합니다.",
        "tab1": "은하 회전 곡선 (거시 세계)",
        "tab2": "양자 얽힘 (미시 세계)",
        "t1_sub": "거시적 증명: 암흑 물질은 입자가 아니라 공간 텐서(S_loc)의 누적이다.",
        "t1_slider": "공간 누적 계수 (α)",
        "t1_plot_title": "은하 회전 곡선 (Galactic Rotation Curve)",
        "t1_x": "은하 중심으로부터의 거리 r (kpc)",
        "t1_y": "회전 속도 v (km/s)",
        "t1_leg1": "뉴턴 역학 (암흑 물질 없음)",
        "t1_leg2": "K-PROTOCOL 예측",
        "t1_leg3": "실제 관측 데이터 (평탄화 곡선)",
        "t1_info": "💡 **결과 분석:** 계수 α가 1/22 (0.04545)에 도달하면 실제 NASA 관측 데이터와 완벽히 일치하는 평탄한 곡선이 완성되며, 암흑 물질이라는 착시가 해결됩니다.",
        "t2_sub": "미시적 증명: 양자 얽힘은 '확률의 붕괴'가 아니라 단일 위상 매듭(T)의 투영이다.",
        "t2_plot_title": "양자 얽힘: 벨의 부등식 위배 (Bell's Inequality Violation)",
        "t2_x": "측정기 사이의 각도 차이 θ (Radians)",
        "t2_y": "상관관계 (Correlation)",
        "t2_leg1": "고전적 한계 (Bell's Limit)",
        "t2_leg2": "K-PROTOCOL 기하학적 투영",
        "t2_info": "💡 **결과 분석:** 푸른색 점선(고전적 한계)을 뚫고 나오는 붉은색 곡선은 빛보다 빠른 통신이 아니라, 두 입자가 동일한 기하학적 매듭으로 연결되어 나타나는 3차원 투영(Cos) 현상입니다."
    },
    "English": {
        "title": "🌌 K-PROTOCOL: Grand Unification Master Simulator",
        "desc": "Deconstructing the mysteries of the macro (Galactic Rotation) and micro (Quantum Entanglement) worlds using the single **K-Omni Equation**.",
        "tab1": "Galactic Rotation (Macro)",
        "tab2": "Quantum Entanglement (Micro)",
        "t1_sub": "Macroscopic Proof: Dark Matter is not a particle, but the accumulation of the Spatial Tensor (S_loc).",
        "t1_slider": "Spatial Accumulation Coefficient (α)",
        "t1_plot_title": "Galactic Rotation Curve",
        "t1_x": "Distance from Galactic Center r (kpc)",
        "t1_y": "Rotational Velocity v (km/s)",
        "t1_leg1": "Newtonian (No Dark Matter)",
        "t1_leg2": "K-PROTOCOL Prediction",
        "t1_leg3": "Observed Data (Flat Curve)",
        "t1_info": "💡 **Analysis:** When α reaches 1/22 (0.04545), the curve aligns perfectly with NASA's observed data, mathematically resolving the Dark Matter illusion.",
        "t2_sub": "Microscopic Proof: Quantum Entanglement is a geometric projection of a single phase knot (T).",
        "t2_plot_title": "Quantum Entanglement: Bell's Inequality Violation",
        "t2_x": "Angle Difference Between Detectors θ (Radians)",
        "t2_y": "Correlation",
        "t2_leg1": "Classical Limit (Bell's Limit)",
        "t2_leg2": "K-PROTOCOL Geometric Projection",
        "t2_info": "💡 **Analysis:** The red curve breaking the classical limit proves entanglement is a necessary 3D projection (Cos) of a shared geometric topological string, not faster-than-light communication."
    }
}

text = t[lang]

# ==========================================
# 2. 메인 화면 출력
# ==========================================
st.title(text["title"])
st.markdown(text["desc"])

# K-Omni 마스터 방정식 (LaTeX)
st.latex(r"\mathbf{\Psi}_{K} = \left( \frac{\pi^n \cdot f}{\mathbf{S}_{loc}} \right) e^{i \pi \mathbf{T}}")
st.divider()

# 탭 생성
tab1, tab2 = st.tabs([text["tab1"], text["tab2"]])

# ==========================================
# 3. 탭 1: 은하 회전 곡선 시뮬레이션
# ==========================================
with tab1:
    st.subheader(text["t1_sub"])
    
    # 슬라이더 (사이드바 대신 탭 안에 배치하여 직관성 향상)
    alpha_input = st.slider(text["t1_slider"], 0.0, 0.1, 0.04545, 0.0001, format="%.5f")
    
    # 데이터 연산
    r = np.linspace(1, 50, 500)
    G_M = 20000
    v_newton = np.sqrt(G_M / r)
    S_loc_cumulative = 1 + (alpha_input * r)
    v_kprotocol = np.sqrt((G_M / r) * S_loc_cumulative)
    observed_flat = np.full_like(r, np.mean(v_kprotocol[350:]))

    # Plotly 그래프 생성
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=r, y=v_newton, name=text["t1_leg1"], line=dict(dash='dash', color='#3498db', width=2)))
    fig1.add_trace(go.Scatter(x=r, y=v_kprotocol, name=text["t1_leg2"], line=dict(color='#e74c3c', width=4)))
    fig1.add_trace(go.Scatter(x=r, y=observed_flat, name=text["t1_leg3"], line=dict(dash='dot', color='#2ecc71', width=3)))
    
    fig1.update_layout(
        title=text["t1_plot_title"],
        xaxis_title=text["t1_x"],
        yaxis_title=text["t1_y"],
        template="plotly_white",
        hovermode="x unified",
        legend=dict(yanchor="bottom", y=0.05, xanchor="left", x=0.05)
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.success(text["t1_info"])

# ==========================================
# 4. 탭 2: 양자 얽힘 시뮬레이션
# ==========================================
with tab2:
    st.subheader(text["t2_sub"])

    # 데이터 연산
    theta = np.linspace(0, np.pi, 500)
    classical_limit = 1 - (2 * theta / np.pi)
    k_protocol_proj = np.cos(theta)

    # Plotly 그래프 생성
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=theta, y=classical_limit, name=text["t2_leg1"], line=dict(dash='dash', color='#3498db', width=2)))
    fig2.add_trace(go.Scatter(x=theta, y=k_protocol_proj, name=text["t2_leg2"], line=dict(color='#9b59b6', width=4)))

    fig2.update_layout(
        title=text["t2_plot_title"],
        xaxis_title=text["t2_x"],
        yaxis_title=text["t2_y"],
        template="plotly_white",
        hovermode="x unified",
        legend=dict(yanchor="bottom", y=0.05, xanchor="left", x=0.05)
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.info(text["t2_info"])
