class OptionChainBrain:
    """Squad O: Option Chain PCR & Volatility Brain"""
    def evaluate(self, pcr_ratio: float, vix: float) -> dict:
        if pcr_ratio >= 1.2:
            signal = 1  # Bullish Put Writing
            reason = "High PCR (Strong Put Support)"
        elif pcr_ratio <= 0.8:
            signal = -1 # Bearish Call Writing
            reason = "Low PCR (Heavy Call Resistance)"
        else:
            signal = 0  # Neutral
            reason = "PCR Neutral Zone"
            
        return {"signal": signal, "confidence": 0.90, "reason": reason}
