import time
from core.event_bus import event_bus

class SquadSSmartExecutor:
    """Squad S: Paper Trading Execution & Real-Time PnL Tracker"""
    def __init__(self, initial_capital=10000.0):
        self.capital = initial_capital
        self.balance = initial_capital
        self.positions = []
        self.closed_trades = []
        
        # Subscribe to Level-2 Stream for price tick updates
        event_bus.subscribe("level2_depth_update", self.on_price_update)

    def execute_paper_trade(self, signal_data):
        # Allow max 3 open positions at a time
        if len(self.positions) >= 3:
            print("⚠️ [SQUAD S] Max open positions reached. Skipping trade execution.")
            return

        trade_size = 1000.0  # $1,000 USDT per trade
        
        position = {
            "id": int(time.time()),
            "symbol": signal_data['symbol'],
            "type": signal_data['type'],
            "entry_price": signal_data['entry'],
            "stop_loss": signal_data['stop_loss'],
            "take_profit": signal_data['take_profit'],
            "amount": trade_size,
            "entry_time": time.time()
        }

        self.positions.append(position)
        print(f"📈 [SQUAD S PAPER TRADE OPENED] {position['type']} {position['symbol']} @ ${position['entry_price']}")

    def on_price_update(self, data):
        current_price = data['top_ask'] if data['imbalance'] > 0 else data['top_bid']
        
        # Check active positions for SL/TP hits
        remaining_positions = []
        for pos in self.positions:
            pnl = 0.0
            closed = False
            exit_reason = ""

            if pos['type'] == "BUY":
                if current_price >= pos['take_profit']:
                    closed = True
                    exit_reason = "TAKE_PROFIT"
                    pnl = (pos['amount'] / pos['entry_price']) * (pos['take_profit'] - pos['entry_price'])
                elif current_price <= pos['stop_loss']:
                    closed = True
                    exit_reason = "STOP_LOSS"
                    pnl = (pos['amount'] / pos['entry_price']) * (pos['stop_loss'] - pos['entry_price'])

            elif pos['type'] == "SELL":
                if current_price <= pos['take_profit']:
                    closed = True
                    exit_reason = "TAKE_PROFIT"
                    pnl = (pos['amount'] / pos['entry_price']) * (pos['entry_price'] - pos['take_profit'])
                elif current_price >= pos['stop_loss']:
                    closed = True
                    exit_reason = "STOP_LOSS"
                    pnl = (pos['amount'] / pos['entry_price']) * (pos['entry_price'] - pos['stop_loss'])

            if closed:
                self.balance += pnl
                closed_record = {
                    "symbol": pos['symbol'],
                    "type": pos['type'],
                    "entry": pos['entry_price'],
                    "exit": current_price,
                    "pnl": round(pnl, 2),
                    "reason": exit_reason
                }
                self.closed_trades.append(closed_record)
                print(f"🎯 [SQUAD S TRADE CLOSED] {exit_reason} | PnL: ${round(pnl, 2)}")
            else:
                remaining_positions.append(pos)

        self.positions = remaining_positions

    def get_performance_summary(self):
        total_trades = len(self.closed_trades)
        winning_trades = sum(1 for t in self.closed_trades if t['pnl'] > 0)
        win_rate = round((winning_trades / total_trades * 100), 2) if total_trades > 0 else 0.0
        total_pnl = round(self.balance - self.capital, 2)

        return {
            "initial_capital": f"${self.capital}",
            "current_balance": f"${round(self.balance, 2)}",
            "total_pnl": f"${total_pnl}",
            "total_trades": total_trades,
            "win_rate": f"{win_rate}%",
            "active_positions": len(self.positions)
        }

# Global Smart Executor Instance
smart_executor = SquadSSmartExecutor()
