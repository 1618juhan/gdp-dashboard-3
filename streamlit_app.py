import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

# ---------------------------
# 1. 앱 제목
# ---------------------------
st.set_page_config(page_title="Coral Dashboard", layout="centered")
st.title("🌍 산호초 백화 현황 대시보드")

# ---------------------------
# 2. 연도 입력 섹션
# ---------------------------
st.header("🔢 연도 선택")
selected_year = st.number_input(
    label="연도 선택 (1980~2024)",
    min_value=1980,
    max_value=2024,
    value=2000,
    step=1
)

# ---------------------------
# 3. 산호초 백화 데이터 계산
# ---------------------------
years_known = np.array([1980, 1998, 2010, 2015, 2024])
bleach_known = np.array([5, 21, 37, 68, 84])  # %

years = np.arange(1980, 2025)
interp = PchipInterpolator(years_known, bleach_known)
bleach = np.clip(interp(years), 0, 100)
remain = 100 - bleach

df = pd.DataFrame({
    "연도": years,
    "백화율(%)": np.round(bleach, 2),
    "남은 산호(%)": np.round(remain, 2)
})

# ---------------------------
# 4. 선택 연도 데이터 표시
# ---------------------------
st.write(f"**{selected_year}년 산호초 상태:**")
st.dataframe(df[df["연도"] == selected_year])

# ---------------------------
# 5. 전체 데이터 보기
# ---------------------------
with st.expander("📊 전체 1980~2024년 데이터 보기"):
    st.dataframe(df)

# ---------------------------
# 6. 그래프
# ---------------------------
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(years, bleach, label="백화(%)", color="tomato", marker="o")
ax.plot(years, remain, label="남은 산호(%)", color="royalblue", marker="o")
ax.set_ylim(0, 100)
ax.set_xlabel("연도")
ax.set_ylabel("비율(%)")
ax.set_title("지구 전체 산호초 백화 추이 (1980–2024)")
ax.legend()
ax.grid(alpha=0.3)

# 선택 연도 강조
idx = np.where(years == selected_year)[0][0]
ax.scatter(selected_year, bleach[idx], color="red", s=100, zorder=5)
ax.text(selected_year, bleach[idx]+3, f"{bleach[idx]:.1f}%", color="red")

st.pyplot(fig)

# ---------------------------
# 7. 설명
# ---------------------------
st.markdown("""
**해설**  
- 1980년 이후 지구 산호초의 백화 현상은 급격히 증가하고 있습니다.  
- 연도를 선택하면 해당 시점의 산호 상태를 바로 확인할 수 있습니다.  
- 전체 데이터를 확인하려면 '전체 데이터 보기'를 펼쳐보세요.
""")