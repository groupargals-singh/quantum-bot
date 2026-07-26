import os
from typing import Dict, Any

class RealtimeDashboard:
    """Institutional Real-Time Terminal P&L Dashboard"""
    
    @staticmethod
    def render_portfolio(positions: Dict[str, Any], realized_pnl: float, capital: float):
        print("\n" + "="*60)
        print("📊 QUANTUM BOT - REAL-TIME LIVE PORTFOLIO & P&L DASHBOARD")
        print("="*60)
        
        if not positions:
            print("  [ NO ACTIVE POSITIONS | SCANNING FOR OPPORTUNITIES... ]")
        else:
            print(f"{'SYMBOL':<10} | {'QTY':<5} | {'ENTRY':<8} | {'SL':<8} | {'TARGET':<8}")
            print("-" * 60)
            for sym, pos in positions.items():
                print(f"{sym:<10} | {pos['qty']:<5} | ₹{pos['buy_price']:<7.1f} | ₹{pos['stop_loss']:<7.1f} | ₹{pos['target']:<7.1f}")
        
        print("="*60)
        print(f"💰 Available Capital : ₹{capital:,.2f}")
        print(f"📈 Realized P&L     : ₹{realized_pnl:,.2f}")
        print("="*60 + "\n")
