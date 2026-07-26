class SwarmConsensusEngine:
    """
    Master Consensus Engine:
    Combines weighted signals from Squad B, Squad G, Squad M, and Squad O.
    """
    def __init__(self):
        # Squad Weights
        self.weights = {
            "squad_o_options": 0.35, # Highest weightage for Options/PCR
            "squad_b_tech": 0.30,    # Technicals
            "squad_g_news": 0.20,    # News Sentiment
            "squad_m_orderflow": 0.15 # Orderflow
        }

    def compute_master_consensus(self, tech_sig: int, news_sig: int, option_sig: int, orderflow_sig: int) -> dict:
        weighted_score = (
            (option_sig * self.weights["squad_o_options"]) +
            (tech_sig * self.weights["squad_b_tech"]) +
            (news_sig * self.weights["squad_g_news"]) +
            (orderflow_sig * self.weights["squad_m_orderflow"])
        )

        if weighted_score > 0.25:
            final_signal = 1  # STRONG BUY
        elif weighted_score < -0.25:
            final_signal = -1 # STRONG SELL
        else:
            final_signal = 0  # HOLD / NO TRADE

        return {
            "master_signal": final_signal,
            "weighted_score": round(weighted_score, 3),
            "consensus": "BULLISH" if final_signal == 1 else ("BEARISH" if final_signal == -1 else "NEUTRAL")
        }
