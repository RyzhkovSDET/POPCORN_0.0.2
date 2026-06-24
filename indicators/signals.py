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
        return "🟢 STRG BUY"
    elif score > 60:
        return "🟡 BUY"
    elif score < 20:
        return "🔴 STRG SELL"
    elif score < 40:
        return "🟠 SELL"
    return "⚪ HOLD"