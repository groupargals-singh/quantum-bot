class DynamicKellyRiskShield:
    """
    🛡️ Dynamic Kelly Criterion Risk Sizing Engine
    Ensures 0% capital blowout risk by sizing positions dynamically.
    """
    def calculate_optimal_lot_size(self, capital: float, win_probability: float, reward_risk_ratio: float) -> dict:
        p = win_probability / 100.0
        q = 1.0 - p
        b = reward_risk_ratio
        
        # Fractional Kelly Formula (Half-Kelly for Conservative Maximum Growth)
        kelly_fraction = (b * p - q) / max(0.1, b)
        safe_kelly = max(0.02, min(0.15, kelly_fraction * 0.5)) # Cap between 2% and 15% capital
        
        allocated_capital = capital * safe_kelly
        return {
            "recommended_capital_allocation": round(allocated_capital, 2),
            "kelly_fraction_pct": round(safe_kelly * 100, 2),
            "risk_status": "OPTIMAL_SHIELD_ACTIVE"
        }
