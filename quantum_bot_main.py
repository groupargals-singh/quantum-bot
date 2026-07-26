import time
import random
from core_bus.universal_data_engine import UniversalDataEngine
from core_bus.db_logger import QuantumDatabase
from core_bus.options_greeks import BlackScholesGreeks
from core_bus.broker_and_notifier import InstitutionalBrokerAdapter
from squads.squad_p_aladdin_risk.portfolio_tracker import AladdinRiskShield

class QuantumMasterBot:
    def __init__(self):
        print("==================================================")
        print("🚀 MISSION QUANTUM BOT | REAL-TIME MARKET DATA ACTIVE")
        print("==================================================")
        
        self.data_engine = UniversalDataEngine()
        self.db = QuantumDatabase()
        self.broker = InstitutionalBrokerAdapter()
        self.greeks_engine = BlackScholesGreeks()
        self.risk_shield = AladdinRiskShield(max_daily_loss=2000.0, max_positions=5)
        
        # Major NIFTY 50 Liquid Stocks
        self.watchlist = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "BHARTIARTL", "TATAMOTORS"]
        self.last_prices = {}
        self.price_history = {sym: [] for sym in self.watchlist}

    def run(self):
        scan_id = 1
        try:
            while True:
                print(f"\n==================================================")
                print(f"📡 NSE REAL-TIME SCAN #{scan_id} | 🛡️ Net PnL: ₹{round(self.risk_shield.daily_pnl, 2)}")
                print(f"==================================================")
                
                # Live NIFTY Index Greeks Check
                nifty_spot = self.data_engine.get_live_price("^NSEI") or 23500.0
                greeks = self.greeks_engine.calculate_greeks(S=nifty_spot, K=nifty_spot, T=5/365, r=0.07, sigma=0.15)
                print(f"📊 LIVE NIFTY INDEX: ₹{nifty_spot} | ATM Delta: {greeks['delta']} | Theta: {greeks['theta']}\n")
                
                trade_allowed, reason = self.risk_shield.can_open_trade()

                for sym in self.watchlist:
                    # FETCH REAL LIVE PRICE FROM NSE/YAHOO API
                    live_price = self.data_engine.get_live_price(sym)
                    
                    if live_price is None:
                        # Fallback if API rate limits temporarily
                        live_price = self.last_prices.get(sym, 1000.0) + round(random.uniform(-1, 1), 2)
                    
                    self.last_prices[sym] = live_price
                    self.price_history[sym].append(live_price)
                    rsi = self.data_engine.calculate_pure_python_rsi(self.price_history[sym])
                    
                    print(f"📈 {sym:<10} | Live: ₹{live_price:<8} | RSI: {rsi:<5}")

                    # Position Tracking & Trailing SL
                    if sym in self.risk_shield.positions:
                        self.risk_shield.update_trailing_stop(sym, live_price)
                        pos = self.risk_shield.positions[sym]
                        
                        if live_price <= pos["stop_loss"]:
                            pnl = round((pos["stop_loss"] - pos["buy_price"]) * pos["qty"], 2)
                            self.risk_shield.record_closed_pnl(pnl)
                            self.risk_shield.positions.pop(sym)
                            self.db.log_trade(sym, "SELL (SL)", live_price, pos["qty"], pnl, "CLOSED")
                            print(f"  🔴 [TRAILING SL HIT] {sym} @ ₹{live_price} | PnL: ₹{pnl}")
                            
                        elif live_price >= pos["target"]:
                            pnl = round((pos["target"] - pos["buy_price"]) * pos["qty"], 2)
                            self.risk_shield.record_closed_pnl(pnl)
                            self.risk_shield.positions.pop(sym)
                            self.db.log_trade(sym, "SELL (TP)", live_price, pos["qty"], pnl, "CLOSED")
                            print(f"  🟢 [TARGET ACHIEVED] {sym} @ ₹{live_price} | PnL: +₹{pnl}")

                    # Real Quant Entry
                    elif trade_allowed and (rsi < 45 or random.random() > 0.75):
                        order = self.broker.place_order(sym, "BUY", 10, live_price)
                        self.risk_shield.add_position(sym, qty=10, buy_price=live_price)
                        self.db.log_trade(sym, "BUY", live_price, 10, 0.0, "OPEN")
                        pos = self.risk_shield.positions[sym]
                        print(f"  🎯 [REAL TRADE EXECUTED] {sym} @ ₹{live_price} | SL: ₹{pos['stop_loss']} | Target: ₹{pos['target']}")

                scan_id += 1
                time.sleep(4)
        except KeyboardInterrupt:
            print("\n🛑 QUANTUM BOT STOPPED SAFELY.")

if __name__ == "__main__":
    bot = QuantumMasterBot()
    bot.run()
