import os
import requests
from src.core.event_bus import event_bus
from src.strategies.risk_shield import risk_shield
from src.core.state import system_state
from src.strategies.technical_brain import technical_brain
from src.execution.smart_executor import smart_executor

class MasterCommander:
    """APEX Orchestrator & Multi-Agent Consensus Swarm"""
    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        self.last_signal_time = 0
        self.cooldown_seconds = 45

        event_bus.subscribe("level2_depth_update", self.on_market_tick)

    def broadcast_consensus_signal(self, signal_data, consensus_score):
        smart_executor.execute_paper_trade(signal_data)

        if not self.bot_token or not self.chat_id:
            return

        msg = (
            f"👑 *ENTERPRISE QUANTUM CONSENSUS* 👑\n\n"
            f"🎯 *Symbol:* `{signal_data['symbol']}`\n"
            f"🚦 *Decision:* `{signal_data['type']}`\n"
            f"🔥 *Consensus Score:* `{consensus_score}%`\n\n"
            f"💵 *Entry:* `${signal_data['entry']}`\n"
            f"🛑 *Stop Loss:* `${signal_data['stop_loss']}`\n"
            f"🎯 *Take Profit:* `${signal_data['take_profit']}`\n"
            f"📊 *RR Ratio:* `{signal_data['rr_ratio']}`\n\n"
            f"⚡ *Execution Engine:* Position Opened"
        )

        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": msg, "parse_mode": "Markdown"}
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"❌ [MASTER COMMANDER ERROR] {e}")

    def on_market_tick(self, data):
        if system_state.is_paused:
            return

        current_time = data['timestamp']
        price = data['top_ask'] if data['imbalance'] > 0 else data['top_bid']

        technical_brain.update_price(price)

        if current_time - self.last_signal_time < self.cooldown_seconds:
            return

        imb = data['imbalance']
        tech_trend, tech_score = technical_brain.analyze_momentum()

        votes_buy = 0
        votes_sell = 0

        if imb > 0.30:
            votes_buy += 1
        elif imb < -0.30:
            votes_sell += 1

        if tech_trend == "BULLISH":
            votes_buy += 1
        elif tech_trend == "BEARISH":
            votes_sell += 1

        signal_type = None
        consensus_score = 0.0

        if votes_buy >= 2:
            signal_type = "BUY"
            consensus_score = round(((imb * 100) + tech_score) / 2, 1)
        elif votes_sell >= 2:
            signal_type = "SELL"
            consensus_score = round(((abs(imb) * 100) + tech_score) / 2, 1)

        if signal_type:
            valid, verified_signal = risk_shield.validate_signal(
                data['symbol'], signal_type, price, imb
            )
            if valid and consensus_score >= 60.0:
                self.last_signal_time = current_time
                self.broadcast_consensus_signal(verified_signal, consensus_score)

master_commander = MasterCommander()
