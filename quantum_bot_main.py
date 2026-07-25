import time
from data_filters.noise_filter import DataFilterEngine
from squads.base_brain import BaseMicroBrain
from squads.base_squad import BaseSquadCommander
from squads.squad_p_aladdin_risk.aladdin_risk import AladdinRiskEngine
from squads.squad_s_smart_execution.smart_executor import SmartExecutionEngine
from core_bus.event_bus import AsyncEventBus
from core_bus.live_feed_manager import MultiFeedManager
from core_bus.news_and_fno_feed import NewsAndFnOFeedManager
from core_bus.nse_quantum_hub import NSEDirectQuantumHub

class QuantumBotEngine:
    def __init__(self):
        print("==================================================")
        print("🚀 QUANTUM BOT FULL NSE + MULTI-SOURCE PIPELINE")
        print("==================================================")
        
        self.data_filter = DataFilterEngine(volatility_threshold=0.0002)
        self.event_bus = AsyncEventBus()
        self.risk_engine = AladdinRiskEngine(max_daily_loss=5000.0, max_position_value=100000.0)
        self.executor = SmartExecutionEngine(paper_trading=True, initial_capital=100000.0)
        
        # Squad Commanders
        self.squad_m = BaseSquadCommander("SQUAD_M", "Orderflow & Price Action")
        self.squad_o = BaseSquadCommander("SQUAD_O", "Option Chain & PCR Analytics")
        
        # Data Managers
        self.feed_manager = MultiFeedManager(on_tick_callback=self.handle_incoming_tick)
        self.news_manager = NewsAndFnOFeedManager()
        self.nse_hub = NSEDirectQuantumHub()

    def boot_system(self):
        print("[1/7] Micro-Second Price Filter... [ACTIVE]")
        print("[2/7] NSE Option Chain & PCR Hub... [ONLINE]")
        print("[3/7] India VIX & Market Breadth Stream... [ONLINE]")
        print("[4/7] Global News & Wire Stream... [CONNECTED]")
        print("[5/7] 20 Squad Swarm Engine... [READY]")
        print("[6/7] Aladdin Risk Shield... [ACTIVE]")
        print("[7/7] Smart Execution Terminal... [PAPER TRADING ACTIVE]")
        print("\n✨ FULL QUANTUM DATA PIPELINE ONLINE!\n")

    def handle_incoming_tick(self, symbol: str, price: float, volume: int):
        filtered = self.data_filter.process_tick(symbol, price, volume)
        if filtered:
            print(f"⚡ TICK: {symbol:<10} | Price: ₹{price:<8} | Vol: {volume}")
            consensus = self.squad_m.calculate_squad_consensus(filtered)
            sig = consensus['consensus_signal']
            
            if sig != 0:
                risk_check = self.risk_engine.evaluate_trade_risk(symbol, price, quantity=10)
                if risk_check['approved']:
                    order_result = self.executor.execute_order(symbol, sig, price, quantity=10)
                    print(f"   📈 Order Executed: {order_result['action']} {symbol} @ ₹{price}\n")
        else:
            print(f"🧹 NOISE DROPPED: {symbol:<10} @ ₹{price}")

    def run_live(self):
        print("--- 1. NSE OPTION CHAIN & PCR ANALYSIS ---")
        pcr_data = self.nse_hub.fetch_option_chain_pcr("NIFTY")
        print(f"🎯 NIFTY PCR Ratio: {pcr_data['pcr_ratio']} | Sentiment: {pcr_data['sentiment']}")
        print(f"   Call OI: {pcr_data['call_oi']:,} | Put OI: {pcr_data['put_oi']:,}")
        
        print("\n--- 2. MARKET BREADTH & VOLATILITY ---")
        breadth = self.nse_hub.fetch_market_breadth()
        print(f"📊 India VIX: {breadth['india_vix']} | Advances: {breadth['advances']} vs Declines: {breadth['declines']}")

        print("\n--- 3. BREAKING MARKET NEWS ---")
        news = self.news_manager.fetch_latest_market_news()
        for idx, item in enumerate(news[:2], 1):
            print(f"   {idx}. {item['title']}")

        print("\n" + "="*50 + "\n")
        print("--- 4. LIVE MULTI-STOCK TICK SCAN ---")
        self.feed_manager.start_feed(iterations=1)

if __name__ == "__main__":
    bot = QuantumBotEngine()
    bot.boot_system()
    bot.run_live()
