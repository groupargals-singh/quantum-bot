import time
from core.event_bus import event_bus
from core.database import save_trade_db, update_trade_exit_db

class SquadSSmartExecutor:
    """Squad S: Paper Trading with Dynamic Dynamic Compound Sizing"""
    def __init__(self, initial_capital=10000.0):
        self.capital = initial_capital
        self.balance = initial_capital
        self.positions = []
        self.closed_trades = []
        
        event_bus.subscribe("level2_depth_update", self.on_price_update)

    def execute_paper_trade(self, signal_data):
        if len(self.positions) >= 5:
            print("⚠️ [SQUAD S] Max open multi-asset positions reached.")
            return

        # Dynamic Risk Sizing: Allocate 10% of total balance per trade
        trade_size = round(self.balance * 0.10, 2)
        trade_id = int(time.time() * 1000)
        
        position = {
            "id": trade_id,
            "symbol": signal_data['symbol'],
            "type": signal_data['type'],
            "entry_price": signal_data['entry'],
            "stop_loss": signal_data['stop_loss'],
            "take_profit": signal_data['take_profit'],
            "amount": trade_size,
            "entry_time": time.time()
        }

        self.positions.append(position)
        save_trade_db(
            signal_data['symbol'], signal_data['type'], 
            signal_data['entry'], signal_data['stop_loss'], 
            signal_data['take_profit'], status="OPEN"
        )
        print(f"📈 [SQUAD S DYNAMIC TRADE] {position['type']} {position['symbol']} | Size: ${trade_size} USDT @ ${position['entry_price']}")

    def on_price_update(self, data):
        symbol = data['symbol']
        current_price = data['top_ask'] if data['imbalance'] > 0 else data['top_bid']
        
        remaining_positions = []
        for pos in self.positions:
            if pos['symbol'] != symbol:
                remaining_positions.append(pos)
                continue

            pnl = 0.0
            closed = False
            exit_reason = ""

            if pos['type'] == "BUY":
                new_sl = round(current_price * 0.995, 2)
                if new_sl > pos['stop_loss']:
                    pos['stop_loss'] = new_sl

                if current_price >= pos['take_profit']:
                    closed = True
                    exit_reason = "TAKE_PROFIT"
                    pnl = (pos['amount'] / pos['entry_price']) * (pos['take_profit'] - pos['entry_price'])
                elif current_price <= pos['stop_loss']:
                    closed = True
                    exit_reason = "TRAILING_STOP_LOSS"
                    pnl = (pos['amount'] / pos['entry_price']) * (pos['stop_loss'] - pos['entry_price'])

            elif pos['type'] == "SELL":
                new_sl = round(current_price * 1.005, 2)
                if new_sl < pos['stop_loss']:
                    pos['stop_loss'] = new_sl

                if current_price <= pos['take_profit']:
                    closed = True
                    exit_reason = "TAKE_PROFIT"
                    pnl = (pos['amount'] / pos['entry_price']) * (pos['entry_price'] - pos['take_profit'])
                elif current_price >= pos['stop_loss']:
                    closed = True
                    exit_reason = "TRAILING_STOP_LOSS"
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
                update_trade_exit_db(pos['id'], current_price, round(pnl, 2), exit_reason)
                print(f"🎯 [SQUAD S TRADE CLOSED] {symbol} | {exit_reason} | PnL: ${round(pnl, 2)}")
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

smart_executor = SquadSSmartExecutor()
