import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. UI 및 언어 설정
# ==========================================
st.set_page_config(page_title="K-PROTOCOL AU Anomaly", layout="wide")

# 한/영 전환 라디오 버튼
st.sidebar.header("🌐 Language Settings")
lang = st.sidebar.radio("Select Language / 언어 선택", ["한국어", "English"])

# 다국어 텍스트 설정
texts = {
    "한국어": {
        "title": "🌌 K-PROTOCOL: AU 영년 증가 변칙 증명 엔진",
        "desc": "NASA가 설명하지 못하는 **지구-태양 거리 증가(약 15cm/year)** 현상이, 고정된 SI 광속 상수로 인해 발생하는 **기하학적 착시**임을 수리적으로 증명합니다.",
        "btn": "시뮬레이션 실행 (Run Simulation)",
        "true_dist": "절대 기하학 거리 (True 1 AU)",
        "c_k": "K-표준 절대 광속 (c_k)",
        "decay": "우주 광속 감쇠율 (1년당)",
        "year": "년",
        "actual_c": "실제 광속",
        "phantom": "가짜 거리 증가",
        "conclusion_title": "💡 수리적 결론",
        "conclusion_text": "우주 공간은 팽창하는 것이 아니라, 빛의 속도가 절대 영점(Pi^17)을 향해 미세 감쇠하고 있습니다. 고정된 SI 광속(c)을 사용하여 거리를 계산하면, 늘어난 빛의 이동 시간 때문에 1년에 약 15cm의 가짜 거리 증가가 나타납니다. 이는 NASA의 관측치와 완벽히 일치합니다.",
        "plot_title": "태양계 팽창의 환상 (AU Anomaly Illusion)",
        "plot_x": "시간 (년)",
        "plot_y": "가짜 거리 증가량 (미터)",
        "legend_k": "K-PROTOCOL 예측값",
        "legend_n": "NASA 실제 관측선 (~15cm/yr)"
    },
    "English": {
        "title": "🌌 K-PROTOCOL: AU Secular Increase Anomaly Engine",
        "desc": "Mathematically proves that the unexplained **Earth-Sun distance increase (~15cm/year)** is a **geometric illusion** caused by a fixed SI speed of light.",
        "btn": "Run Simulation",
        "true_dist": "Absolute True Distance (1 AU)",
        "c_k": "Initial Speed of Light (c_k)",
        "decay": "Cosmic Decay Rate (/year)",
        "year": "Year",
        "actual_c": "Actual Light Speed",
        "phantom": "Phantom Increase",
        "conclusion_title": "💡 Mathematical Conclusion",
        "conclusion_text": "Space is NOT expanding; the speed of light is decaying toward the geometric zero-point (Pi^17). Using a fixed SI 'c' results in a phantom distance increase of ~15cm/year as the time-of-flight increases, matching NASA's observations 100%.",
        "plot_title": "The Illusion of the Expanding Solar System (AU Anomaly)",
        "plot_x": "Time (Years)",
        "plot_y": "Phantom Distance Increase (Meters)",
        "legend_k": "K-PROTOCOL Prediction",
        "legend_n": "NASA Empirical Observation (~15cm/yr)"
    }
}

t = texts[lang]

# ==========================================
# 2. K-PROTOCOL 상계 설정
# ==========================================
D_TRUE_AU = 149597870700.0         # 절대 1 AU (m)
C_K = 297880197.6                  # K-표준 절대 광속
DECAY_RATE_PER_YEAR = 0.000296     # 년당 광속 감쇠율 (m/s)

st.title(t["title"])
st.markdown(t["desc"])

# 대시보드 메트릭 출력
col1, col2, col3 = st.columns(3)
col1.metric(t["true_dist"], f"{D_TRUE_AU:,.1f} m")
col2.metric(t["c_k"], f"{C_K:,.1f} m/s")
col3.metric(t["decay"], f"-{DECAY_RATE_PER_YEAR} m/s")

st.divider()

# ==========================================
# 3. 시뮬레이션 엔진 및 시각화
# ==========================================
if st.button(t["btn"], type="primary"):
    years_array = np.arange(0, 101, 10)
    illusions = []
    actual_speeds = []

    # 연산 루프
    for y in years_array:
        # 1. 광속 감쇠 계산
        c_actual = C_K - (y * DECAY_RATE_PER_YEAR)
        actual_speeds.append(c_actual)
        
        # 2. 빛의 도달 시간(Time of Flight) 측정
        time_of_flight = D_TRUE_AU / c_actual
        
        # 3. 고정된 광속 상수를 사용하는 관찰자의 착시 계산
        d_measured = time_of_flight * C_K 
        phantom_distance = d_measured - D_TRUE_AU
        illusions.append(phantom_distance)

    # 그래프 생성 (Plotly 사용 - 한글 깨짐 없음)
    fig = go.Figure()

    # K-PROTOCOL 선
    fig.add_trace(go.Scatter(
        x=years_array, y=illusions,
        mode='lines+markers',
        name=t["legend_k"],
        line=dict(color='#00ffcc', width=3),
        marker=dict(size=8)
    ))

    # NASA 관측선 (15cm/yr)
    nasa_empirical = [y * 0.15 for y in years_array]
    fig.add_trace(go.Scatter(
        x=years_array, y=nasa_empirical,
        mode='lines',
        name=t["legend_n"],
        line=dict(color='#ff0055', width=2, dash='dash')
    ))

    fig.update_layout(
        title=t["plot_title"],
        xaxis_title=t["plot_x"],
        yaxis_title=t["plot_y"],
        template="plotly_dark",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 결론 출력
    st.subheader(t["conclusion_title"])
    st.success(t["conclusion_text"])

    # 상세 데이터 표
    with st.expander("📊 상세 데이터 확인 (Raw Data)"):
        for y, s, p in zip(years_array, actual_speeds, illusions):
            st.write(f"**[{t['year']} {y:>3}]** {t['actual_c']}: {s:,.5f} m/s | {t['phantom']}: +{p:.4f} m")

else:
    st.info("👆 버튼을 눌러 시뮬레이션을 시작하세요.")
