import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from api.get_data import fetch_data_for_ticker
from storage.coins_storage import load_coins, save_coins

st.set_page_config(layout="wide")

if "coins" not in st.session_state:
    st.session_state.coins = load_coins()

# ================= CONFIG =================
REFRESH_SEC = 10

# ================= HELPERS =================

def rsi_dot(rsi):
    if rsi < 30:
        return "🟦"
    elif rsi < 40:
        return "🟩"
    elif rsi < 60:
        return "🟨"
    elif rsi < 70:
        return "🟧"
    return "🔴"

def rsi_zone(rsi):
    if rsi < 30:
        return "OVS"
    elif rsi < 40:
        return "WKN"
    elif rsi < 60:
        return "NEU"
    elif rsi < 70:
        return "STR"
    return "OVB"

def score_dot(score):
    if score > 80:
        return "🟢"
    elif score > 60:
        return "🟡"
    elif score > 40:
        return "⚪"
    elif score > 20:
        return "🟠"
    return "🔴"

def score_zone(score):
    if score > 80:
        return "STR"
    elif score > 60:
        return "BULL"
    elif score > 40:
        return "NEU"
    elif score > 20:
        return "BEAR"
    return "STRS"

def signal(score):
    if score > 80:
        return "🟢 STRONG BUY"
    elif score > 60:
        return "🟡 BUY"
    elif score < 20:
        return "🔴 STRONG SELL"
    elif score < 40:
        return "🟠 SELL"
    return "⚪ HOLD"

# ================= UI =================

st.title("🍿 POPCORN")

# Quick Guide выровняем с таблицей
left, right = st.columns([5, 5])

with left:
    st.markdown("""
        <style>
            .quick-guide {
                font-size: 0.8em;
                margin-bottom: 20px;
            }
            .quick-guide h2 {
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("📖 Quick Guide")
    st.markdown("""
        <div class="quick-guide">
        <p><strong>Покупка:</strong> RSI — 🟢, Score — 🟡, Signal — 🟢. <strong>Покупка</strong>.</p>
        <p><strong>Продажа:</strong> RSI — 🔴, Score — 🔴, Signal — 🔴. <strong>Продажа</strong>.</p>
        <p><strong>Сводка:</strong></p>
        <ul>
            <li>🟦 OVS <30 Oversold</li>
            <li>🟩 WKN 30-40 Weak</li>
            <li>🟨 NEU 40-60 Neutral</li>
            <li>🟧 STR 60-70 Strong</li>
            <li>🔴 OVB >70 Overbought</li>
        </ul>
        <p><strong>Score:</strong></p>
        <ul>
            <li>🟢 >80 Strong Buy</li>
            <li>🟡 60-80 Buy</li>
            <li>⚪ 40-60 Hold</li>
            <li>🟠 20-40 Sell</li>
            <li>🔴 <20 Strong Sell</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

with right:
    st.subheader("📋 Watchlist")

watchlist = []
for ticker in st.session_state.coins:
    try:
        df = fetch_data_for_ticker(ticker)

        if df.empty:
            continue

        close = df["close"]

        rsi = RSIIndicator(close, window=14).rsi().iloc[-1]
        ema = EMAIndicator(close, window=20).ema_indicator().iloc[-1]

        score = 50

        if rsi < 30:
            score += 20
        elif rsi > 70:
            score -= 20

        if close.iloc[-1] > ema:
            score += 15
        else:
            score -= 15

        watchlist.append(
            {
                "Coin": ticker.replace("USDT", ""),
                "Price": round(close.iloc[-1], 4),
                "RSI": f"{round(rsi, 1)} {rsi_dot(rsi)} {rsi_zone(rsi)}",
                "ScoreValue": score,                "Score": f"{score} {score_dot(score)} {score_zone(score)}",
                "Delete": "❌",
            }
        )
    except Exception as e:
        st.error(f"{ticker}: {e}")

st.write("Монет загружено:", len(watchlist))
watch_df = pd.DataFrame(watchlist)
watch_df = watch_df.sort_values(by="ScoreValue", ascending=False)
display_df = watch_df.drop(columns=["ScoreValue"]).head(10)

# ================= WATCHLIST =================
with right:
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
        height=300
    )

# ================= CHART =================

st.subheader("📈 Chart")

selected = st.selectbox(
    "Select Coin",
    st.session_state.coins
)

chart_df = fetch_data_for_ticker(selected)

if not chart_df.empty:
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=chart_df.index,
            open=chart_df["open"],
            high=chart_df["high"],
            low=chart_df["low"],
            close=chart_df["close"],
            name="Price",
        )
    )
    fig.update_layout(
        height=450, xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= LEGEND =================
st.subheader("📖 Legend")
st.write("""
    🟦 OVS = Oversold
    🟩 WKN = Weak
    🟨 NEU = Neutral
    🟧 STR = Strong
    🔴 OVB = Overbought
""")

# ================= AUTO REFRESH =================
st.caption(f"Auto refresh: {REFRESH_SEC}s")
time.sleep(REFRESH_SEC)
st.rerun()