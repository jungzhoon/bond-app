
import streamlit as st
import pandas as pd

def bond_price(C, F, r, n):
    price = 0
    for t in range(1, n + 1):
        price += C / (1 + r) ** t
    price += F / (1 + r) ** n
    return price

def mac_dur(C, F, r, n):
    price = bond_price(C, F, r, n)
    weighted_sum = 0
    for t in range(1, n + 1):
        weighted_sum += t * C / (1 + r) ** t
    weighted_sum += n * F / (1 + r) ** n
    return weighted_sum / price

def mod_dur(C, F, r, n):
    return mac_dur(C, F, r, n) / (1 + r)

st.title("📈 채권 가격 및 듀레이션 계산기")

st.markdown("금리 변화에 따른 채권 가격과 듀레이션(민감도)를 계산합니다.")

C = st.number_input("💵 연 이자 (Coupon)", value=5.0)
F = st.number_input("💰 액면가 (Face Value)", value=100.0)
n = st.number_input("⏳ 만기 (년)", min_value=1, value=5)
r_percent = st.slider("📉 시장 금리 (%)", 1.0, 15.0, 3.0, 0.1)
r = r_percent / 100

P = bond_price(C, F, r, n)
D = mac_dur(C, F, r, n)
Dm = mod_dur(C, F, r, n)

st.subheader("📊 결과")
st.write(f"**채권 가격**: {P:.2f} 원")
st.write(f"**맥컬리 듀레이션**: {D:.4f} 년")
st.write(f"**수정 듀레이션**: {Dm:.4f} 년")

st.subheader("📈 금리 변화 시뮬레이션")

rates = [i / 100 for i in range(1, 11)]
data = {
    "이자율 (%)": [r * 100 for r in rates],
    "채권 가격": [bond_price(C, F, r, n) for r in rates],
    "맥컬리 듀레이션": [mac_dur(C, F, r, n) for r in rates],
    "수정 듀레이션": [mod_dur(C, F, r, n) for r in rates],
}

df = pd.DataFrame(data)
st.dataframe(df.style.format({"채권 가격": "{:.2f}", "맥컬리 듀레이션": "{:.4f}", "수정 듀레이션": "{:.4f}"}))
