import os
from dotenv import load_dotenv

load_dotenv()

# Binance Configuration
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# BSC/PancakeSwap Configuration
PANCAKESWAP_RPC_URL = os.getenv("PANCAKESWAP_RPC_URL", "https://bsc-dataseed1.binance.org:8545")
PANCAKESWAP_ROUTER = os.getenv("PANCAKESWAP_ROUTER", "0x10ED43C718714eb63d5aA57B78f6c4d9EcF07f33")

# Trading Pairs (High Volume, Low Volatility)
TRADING_PAIRS = {
    "USDT": "0x55d398326f99059fF775485246999027B3197955",
    "BUSD": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
    "USDC": "0x8AC76a51cc950d9822D68b83FE1Ad97B32Cd580d",
    "BNB": "0xbb4CdB9CBd36B01bD1cbaB6f2f092722989998B6",
    "ETH": "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
    "BTC": "0x7130d2A12B9BCbFdE4C59cc14991e5e19a0d1c1d",
}

# Arbitrage Settings
PROFIT_THRESHOLD = float(os.getenv("PROFIT_THRESHOLD", 0.005))  # 0.5%
MIN_USDT_AMOUNT = float(os.getenv("MIN_USDT_AMOUNT", 100))
MAX_SLIPPAGE = float(os.getenv("MAX_SLIPPAGE", 0.02))  # 2%
GAS_PRICE_MULTIPLIER = float(os.getenv("GAS_PRICE_MULTIPLIER", 1.1))

# Monitoring Settings
CHECK_INTERVAL = 5  # seconds
MAX_CONCURRENT_TRADES = 3

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

print("""
╔════════════════════════════════════════════════════════════════╗
║       ARBITRAGE BOT - EN KARLI KONFİGÜRASYON                   ║
╚════════════════════════════════════════════════════════════════╝

🎯 Strateji: Binance ↔ PancakeSwap Arbitrajı
📍 Blockchain: BSC (Binance Smart Chain)
💱 DEX: PancakeSwap (Yüksek Likidite)
💰 Minimum Kar: %0.5

🔄 İşlem Akışı:
1. Binance'de fiyatı kontrol et
2. PancakeSwap'da fiyatı kontrol et
3. Fiyat farkı %0.5+ ise → ARBITRAJ İŞLEMİ
4. Kar ve gaz ücretleri sonrasında hesapla

✅ Desteklenen Token'lar:
   - USDT (Stablecoin - Düşük Volatilite)
   - BUSD (Stablecoin - Düşük Volatilite)
   - USDC (Stablecoin - Düşük Volatilite)
   - BNB, ETH, BTC (Yüksek Likidite)
""")
