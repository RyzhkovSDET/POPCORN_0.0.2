import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

from api.get_data import fetch_data_for_ticker

from storage.coins_storage import (
    load_coins,
    save_coins
)

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

st.subheader("➕ Добавить монету")

new_coin = st.text_input(
    "",
    placeholder="НАЗВАНИЕ МАНЕТЫ"
)
if st.button("Добавить монету в таблицу"):

    new_coin = new_coin.strip().upper()

    if len(new_coin) > 0:

        if not new_coin.endswith("USDT"):
            new_coin = new_coin + "USDT"

        if new_coin not in st.session_state.coins:
            st.session_state.coins.append(new_coin)

            save_coins(
                st.session_state.coins
            )

            st.rerun()

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
                "ScoreValue": score,
                "Score": f"{score} {score_dot(score)} {score_zone(score)}",
                "Signal": signal(score),
                "Delete": "❌"
            }
        )


    except Exception as e:

        st.error(f"{ticker}: {e}")
st.write("Монет загружено:", len(watchlist))
watch_df = pd.DataFrame(watchlist)

watch_df = watch_df.sort_values(
    by="ScoreValue",
    ascending=False
)

display_df = watch_df.drop(columns=["ScoreValue"])
display_df = display_df.head(10)


# ================= WATCHLIST =================

st.subheader("📋 Watchlist")

left, spacer, right = st.columns([3, 1, 3])

st.markdown("""
<style>

/* Таблица занимает всю выделенную ей область */
[data-testid="stDataFrame"] {
    width: 100% !important;
}

/* Coin */
[data-testid="stDataFrame"] th:nth-child(1),
[data-testid="stDataFrame"] td:nth-child(1) {
    min-width: 140px !important;
}

/* Price */
[data-testid="stDataFrame"] th:nth-child(2),
[data-testid="stDataFrame"] td:nth-child(2) {
    min-width: 180px !important;
}

/* RSI */
[data-testid="stDataFrame"] th:nth-child(3),
[data-testid="stDataFrame"] td:nth-child(3) {
    min-width: 220px !important;
}

/* Score */
[data-testid="stDataFrame"] th:nth-child(4),
[data-testid="stDataFrame"] td:nth-child(4) {
    min-width: 220px !important;
}

/* Signal */
[data-testid="stDataFrame"] th:nth-child(5),
[data-testid="stDataFrame"] td:nth-child(5) {
    min-width: 240px !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stHorizontalBlock"]{
    gap:0.4rem;
}
</style>
""", unsafe_allow_html=True)

with left:

    header = st.columns([2, 2, 2, 2, 2, 1])

    header[0].write("Coin")
    header[1].write("Price")
    header[2].write("RSI")
    header[3].write("Score")
    header[4].write("Signal")
    header[5].write("")

    for _, row in display_df.iterrows():

        cols = st.columns([2, 2, 2, 2, 2, 1])

        cols[0].markdown(f"<small>{row['Coin']}</small>", unsafe_allow_html=True)
        cols[1].markdown(f"<small>{row['Price']}</small>", unsafe_allow_html=True)
        cols[2].markdown(f"<small>{row['RSI']}</small>", unsafe_allow_html=True)
        cols[3].markdown(f"<small>{row['Score']}</small>", unsafe_allow_html=True)
        cols[4].markdown(f"<small>{row['Signal']}</small>", unsafe_allow_html=True)

        if cols[5].button(
                "Х",
                key=f"delete_{row['Coin']}"
        ):

            ticker_to_remove = row["Coin"] + "USDT"

            if ticker_to_remove in st.session_state.coins:
                st.session_state.coins.remove(
                    ticker_to_remove
                )

                save_coins(
                    st.session_state.coins
                )

            st.rerun()

with right:

    st.subheader("📖 Quick Guide")

    st.markdown("""
    <div style="
        font-size:14px;
        margin-bottom:15px;
        line-height:1.6;
    ">
        - Покупка-> 🟢 <b>RSI</b> + 🟡 <b>Score</b> = 🟢 <b>BUY</b><br>
        - Продажа-> 🔴 <b>RSI</b> + 🔴 <b>Score</b> = 🔴 <b>SELL</b>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            "<h5 style='margin-bottom:5px;'>RSI</h5>",
            unsafe_allow_html=True
        )

        st.caption("🟦 OVS <30")
        st.caption("🟩 WKN 30-40")
        st.caption("🟨 NEU 40-60")
        st.caption("🟧 STR 60-70")
        st.caption("🔴 OVB >70")

    with c2:

        st.markdown(
            "<h5 style='margin-bottom:5px;'>Score</h5>",
            unsafe_allow_html=True
        )

        st.caption("🟢 >80 Strong Buy")
        st.caption("🟡 60-80 Buy")
        st.caption("⚪ 40-60 Hold")
        st.caption("🟠 20-40 Sell")
        st.caption("🔴 <20 Strong Sell")

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
            name="Price"
        )
    )

    fig.update_layout(
        height=450,
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ================= LEGEND =================


# ================= AUTO REFRESH =================

st.caption(f"Auto refresh: {REFRESH_SEC}s")

time.sleep(REFRESH_SEC)

st.rerun()