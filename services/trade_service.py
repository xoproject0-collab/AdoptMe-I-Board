def calculate_value(pets):
    return sum(p["value"] for p in pets)

def trade_result(offer_value, want_value):
    diff = want_value - offer_value
    if diff > 10:
        return "WIN"
    elif diff < -10:
        return "LOSE"
    return "FAIR"
