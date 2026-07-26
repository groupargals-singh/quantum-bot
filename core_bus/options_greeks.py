import math

class BlackScholesGreeks:
    @staticmethod
    def _norm_cdf(x: float) -> float:
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

    @staticmethod
    def _norm_pdf(x: float) -> float:
        return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

    @classmethod
    def calculate_greeks(cls, S: float, K: float, T: float, r: float, sigma: float, option_type: str = "CALL"):
        if T <= 0 or sigma <= 0:
            return {"price": max(0.0, S - K if option_type == "CALL" else K - S), "delta": 0.5, "gamma": 0.0, "theta": 0.0, "vega": 0.0}

        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        if option_type.upper() == "CALL":
            price = S * cls._norm_cdf(d1) - K * math.exp(-r * T) * cls._norm_cdf(d2)
            delta = cls._norm_cdf(d1)
            theta = (- (S * cls._norm_pdf(d1) * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * cls._norm_cdf(d2)) / 365.0
        else:
            price = K * math.exp(-r * T) * cls._norm_cdf(-d2) - S * cls._norm_cdf(-d1)
            delta = cls._norm_cdf(d1) - 1.0
            theta = (- (S * cls._norm_pdf(d1) * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * cls._norm_cdf(-d2)) / 365.0

        gamma = cls._norm_pdf(d1) / (S * sigma * math.sqrt(T))
        vega = (S * cls._norm_pdf(d1) * math.sqrt(T)) / 100.0

        return {"price": round(price, 2), "delta": round(delta, 3), "gamma": round(gamma, 5), "theta": round(theta, 2), "vega": round(vega, 2)}
