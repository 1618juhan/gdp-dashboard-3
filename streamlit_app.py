import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

# ---------------------------
# 1. 앱 제목
# ---------------------------
st.set_page_config(page_title="GDP & Coral Dashboard", layout="centered")
st.title("🌍 GDP & 산호초 백화 현황 대시보드")

# ---------------------------
# 2. GDP 입력 섹션
# ---------------------------
st.header("💰 최근 GDP 입력")
gdp_value = st.number_input(
    label="최근 GDP (Billion USD)",
    min_value=0.0,
    value=0.0,
    step=1.0,
    format="%.0f",
    help="최근 연도의 GDP(십억 달러 단위)를 입력하세요."
)

st.write(f"입력한 GDP: **{gdp_value:,.0f} B**")

# ---------------------------
# 3. 산호초 백화 데이터 & 그래프
# ---------------------------
st.header("🪸 1980~2024 산호초 백화 추이")

# 기준 데이터 (추정치)
years_known = np.array([1980, 1998, 2010, 2015, 2024])
bleach_known = np.array([5, 21, 37, 68, 84])  # %

years = np.arange(1980, 2025)
interp = PchipInterpolator(years_known, bleach_known)
bleach = np.clip(interp(years), 0, 100)
remain = 100 - bleach

# 데이터프레임 생성
df = pd.DataFrame({
    "연도": years,
    "백화율(%)": np.round(bleach, 2),
    "남은 산호(%)": np.round(remain, 2)
})

# 표 출력
st.dataframe(df.head(10))

# 그래프
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(years, bleach, label="백화(%)", color="tomato", marker="o")
ax.plot(years, remain, label="남은 산호(%)", color="royalblue", marker="o")
ax.set_ylim(0, 100)
ax.set_xlabel("연도")
ax.set_ylabel("비율(%)")
ax.set_title("지구 전체 산호초 백화 추이 (1980–2024)")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)

# ---------------------------
# 4. 설명
# ---------------------------
st.markdown(
    """
    **해설**  
    - 1980년 이후 지구 산호초의 백화 현상은 급격히 증가하고 있습니다.  
    - 2024년에는 약 84%가 백화 영향을 받은 것으로 추정됩니다.  
    - 기후 변화 완화와 해양 보호 정책이 없으면 남아있는 산호도 빠르게 감소할 수 있습니다.
    """
)