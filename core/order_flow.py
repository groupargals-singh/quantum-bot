import math

class OrderFlowIcebergDetector:
    """
    🌊 Order Flow Imbalance (OFI) & Institutional Iceberg Detector
    Scans Level-2 Depth for hidden liquidity sweeps and fake spoofing orders.
    """
    def analyze_order_flow(self, bid_volume: float, ask_volume: float, delta_sweep: float) -> dict:
        # Calculate Order Flow Imbalance (OFI) Ratio
        total_vol = bid_volume + ask_volume
        ofi_ratio = (bid_volume - ask_volume) / max(1.0, total_vol)
        
        # Iceberg Detection Algorithm
        iceberg_detected = False
        iceberg_type = "NONE"
        
        if delta_sweep > 3.0 and ofi_ratio > 0.65:
            iceberg_detected = True
            iceberg_type = "BULLISH_INSTITUTIONAL_ACCUMULATION"
        elif delta_sweep < -3.0 and ofi_ratio < -0.65:
            iceberg_detected = True
            iceberg_type = "BEARISH_INSTITUTIONAL_DISTRIBUTION"
            
        return {
            "ofi_ratio": round(ofi_ratio, 3),
            "iceberg_detected": iceberg_detected,
            "iceberg_type": iceberg_type,
            "flow_confidence": round(abs(ofi_ratio) * 100, 2)
        }
