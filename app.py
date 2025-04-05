import streamlit as st
import pandas as pd
import numpy as np

# ================================
# 離職予兆スコア計算（A社専用ロジック）
# ================================
def calculate_attrition_score(inputs):
    score = 100

    # スコアを下げる要因
    if inputs.get("パルスサーベイQ1_反応") == 1:
        score -= 15
    if inputs.get("動機づけ反応") == 1:
        score -= 15
    if inputs.get("eNPSスコア", 3) <= 2:
        score -= 10
    if inputs.get("満足度_労働条件", 5) <= 3:
        score -= 10
    if inputs.get("満足度_人間関係", 5) <= 3:
        score -= 10
    if inputs.get("満足度_承認", 5) <= 3:
        score -= 10
    if inputs.get("パルスサーベイQ1未回答", 0) == 1:
        score -= 5
    if inputs.get("eNPS未回答", 0) == 1:
        score -= 5

    return max(min(score, 100), 0)

# ================================
# アドバイス生成
# ================================
def generate_advice(inputs):
    messages = []
    if inputs.get("パルスサーベイQ1_反応") == 1:
        messages.append("📌 パルスサーベイQ1が未回答から回答ありに変化しています。本人の状態変化の可能性があるためヒアリングを推奨します。")
    if inputs.get("動機づけ反応") == 1:
        messages.append("📌 動機づけ要因に対して反応が見られました。何か思うことがある可能性があります。")
    if inputs.get("eNPSスコア", 3) <= 2:
        messages.append("📉 eNPSスコアが低いため、職場への不満や不信感があるかもしれません。")
    if inputs.get("満足度_労働条件", 5) <= 3:
        messages.append("💬 労働条件への満足度が低いため、業務内容や待遇面の確認が有効です。")
    if inputs.get("満足度_人間関係", 5) <= 3:
        messages.append("🤝 人間関係に悩みがある可能性があります。職場内コミュニケーションについて確認しましょう。")
    if inputs.get("満足度_承認", 5) <= 3:
        messages.append("👀 承認欲求が満たされていない可能性があります。成果のフィードバックが届いているか確認を。")
    if not messages:
        return "現時点では特に目立った離職リスク要因は見られません。引き続き定期的なフォローを心がけましょう。"
    return "\n\n".join(messages)

# ================================
# Streamlit UI
# ================================
st.set_page_config(page_title="A社様専用 離職予兆スコア", page_icon="🔍", layout="centered")
st.title("🔍 A社様専用 離職予兆スコア診断")

st.header("📋 スタッフ情報の入力")
col1, col2 = st.columns(2)

with col1:
    q1_react = st.selectbox("パルスサーベイQ1の反応あり", ["なし", "あり"])
    motive_react = st.selectbox("動機づけ要因の反応あり", ["なし", "あり"])
    q1_missing = st.checkbox("パルスサーベイQ1 未回答")
    enps_missing = st.checkbox("eNPS 未回答")

with col2:
    enps_score = st.slider("eNPSスコア (1=推奨しない〜5=強く推奨)", 1, 5, 3)
    cond_score = st.slider("満足度（労働条件）", 1, 5, 4)
    rel_score = st.slider("満足度（人間関係）", 1, 5, 4)
    ack_score = st.slider("満足度（承認）", 1, 5, 4)

if st.button("✅ スコアを診断する"):
    inputs = {
        "パルスサーベイQ1_反応": 1 if q1_react == "あり" else 0,
        "動機づけ反応": 1 if motive_react == "あり" else 0,
        "パルスサーベイQ1未回答": int(q1_missing),
        "eNPS未回答": int(enps_missing),
        "eNPSスコア": enps_score,
        "満足度_労働条件": cond_score,
        "満足度_人間関係": rel_score,
        "満足度_承認": ack_score
    }
    score = calculate_attrition_score(inputs)
    advice = generate_advice(inputs)

    st.subheader("📊 離職予兆スコア")
    st.progress(score / 100)
    st.metric(label="スコア", value=f"{score} / 100")

    st.subheader("💡 おすすめ対応")
    st.success(advice)
