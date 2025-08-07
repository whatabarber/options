def generate_enhanced_commentary(alert):
    """Enhanced AI commentary with Greeks analysis"""
    iv = alert["impliedVolatility"]
    vol = alert["volume"]
    oi = alert["openInterest"]
    score = alert["score"]
    days_exp = alert["daysToExpiration"]
    
    # Profitability assessment
    if score >= 80:
        confidence = "HIGH CONFIDENCE"
        emoji = "🎯"
    elif score >= 65:
        confidence = "GOOD SETUP"
        emoji = "✅"
    elif score >= 50:
        confidence = "MODERATE"
        emoji = "⚠️"
    else:
        confidence = "LOW CONFIDENCE"
        emoji = "❌"
    
    # Main analysis
    commentary_parts = [f"{emoji} {confidence}"]
    
    # Volume analysis
    vol_ratio = vol / max(oi, 1)
    if vol_ratio > 3:
        commentary_parts.append("MASSIVE volume surge - potential big move")
    elif vol_ratio > 2:
        commentary_parts.append("Strong volume activity above normal")
    elif vol_ratio > 1.5:
        commentary_parts.append("Elevated volume interest")
    
    # IV analysis
    if iv > 1.0:
        commentary_parts.append("Extreme IV - high risk/reward")
    elif iv > 0.6:
        commentary_parts.append("Elevated IV suggests catalyst")
    elif 0.3 <= iv <= 0.6:
        commentary_parts.append("Balanced IV environment")
    
    # Time analysis
    if days_exp >= 30:
        commentary_parts.append("Good time buffer for thesis")
    elif days_exp >= 21:
        commentary_parts.append("Moderate time decay risk")
    else:
        commentary_parts.append("Short-term play - watch theta")
    
    # Greeks insight
    if "delta" in alert:
        delta_val = abs(alert["delta"])
        if delta_val > 0.6:
            commentary_parts.append("High delta sensitivity")
        elif delta_val > 0.4:
            commentary_parts.append("Good price sensitivity")
    
    return " | ".join(commentary_parts)