import logging
import config
from binance_connector import BinanceConnector
from pancakeswap_connector import PancakeSwapConnector
from datetime import datetime

logger = logging.getLogger(__name__)

class ArbitrageEngine:
    def __init__(self):
        self.binance = BinanceConnector()
        self.pancakeswap = PancakeSwapConnector()
        self.trade_history = []
        self.total_profit = 0

    def check_arbitrage_opportunity(self, base_token, quote_token="USDT"):
        """
        Arbitraj fırsatını kontrol et
        Strateji: Binance'de ucuz al → PancakeSwap'ta pahalıya sat
        """
        try:
            # Binance sembolü oluştur
            binance_symbol = f"{base_token}{quote_token}"
            
            # Binance fiyatını al
            binance_price = self.binance.get_price(binance_symbol)
            if not binance_price:
                return None
            
            # PancakeSwap token adreslerini al
            token_in_addr = config.TRADING_PAIRS.get(quote_token)
            token_out_addr = config.TRADING_PAIRS.get(base_token)
            
            if not token_in_addr or not token_out_addr:
                return None
            
            # PancakeSwap fiyatını al (1 USDT = ? BNB vs)
            amount_in = 1e18  # 1 USDT (18 decimal)
            pancakeswap_output = self.pancakeswap.get_best_price_for_amount(
                token_in_addr,
                token_out_addr,
                int(amount_in)
            )
            
            if not pancakeswap_output:
                return None
            
            pancakeswap_price = pancakeswap_output / amount_in
            
            # Fiyat farkını hesapla
            price_difference = (pancakeswap_price - binance_price) / binance_price
            
            # Gaz maliyetini hesapla
            gas_cost_data = self.pancakeswap.estimate_transaction_cost()
            gas_cost = gas_cost_data['total_cost_usd'] if gas_cost_data else 0
            
            # Net kar hesapla (gaz ücretleri ve işlem ücretleri sonrası)
            net_profit_percentage = price_difference - (gas_cost / 100)  # 100 USDT işlem
            
            opportunity = {
                'base_token': base_token,
                'quote_token': quote_token,
                'binance_price': binance_price,
                'pancakeswap_price': pancakeswap_price,
                'price_difference_percentage': price_difference * 100,
                'net_profit_percentage': net_profit_percentage * 100,
                'gas_cost_usd': gas_cost,
                'timestamp': datetime.now(),
                'is_profitable': net_profit_percentage > config.PROFIT_THRESHOLD
            }
            
            return opportunity
            
        except Exception as e:
            logger.error(f"❌ Arbitraj kontrol edilemedi ({base_token}): {e}")
            return None

    def scan_all_pairs(self):
        """Tüm token çiftlerini tara ve fırsatları bul"""
        opportunities = []
        
        logger.info("🔍 Arbitraj fırsatları taranıyor...")
        
        for base_token in ['BNB', 'ETH', 'BTC']:
            opportunity = self.check_arbitrage_opportunity(base_token, "USDT")
            if opportunity:
                opportunities.append(opportunity)
                
                if opportunity['is_profitable']:
                    logger.warning(f"""
╔════════════════════════════════════════════════════╗
║          💰 KARLII ARBİTRAJ FIRSATI 💰             ║
╚════════════════════════════════════════════════════╝
Token: {opportunity['base_token']}
Binance Fiyat: {opportunity['binance_price']:.8f}
PancakeSwap Fiyat: {opportunity['pancakeswap_price']:.8f}
Fiyat Farkı: {opportunity['price_difference_percentage']:.4f}%
Gaz Maliyeti: ${opportunity['gas_cost_usd']:.2f}
NET KAR: {opportunity['net_profit_percentage']:.4f}% ✅
                    """)
                else:
                    logger.info(f"{base_token}: {opportunity['net_profit_percentage']:.4f}% kar (eşik altında)")
        
        return opportunities

    def calculate_trade_amount(self, profit_opportunity, available_usdt):
        """İşlem miktarını hesapla"""
        if not profit_opportunity['is_profitable']:
            return None
        
        # Minimum işlem miktarı kontrol et
        if available_usdt < config.MIN_USDT_AMOUNT:
            logger.warning(f"❌ Yeterli USDT yok: {available_usdt} < {config.MIN_USDT_AMOUNT}")
            return None
        
        trade_amount = min(available_usdt, 1000)  # Max 1000 USDT per işlem
        
        return {
            'amount_usdt': trade_amount,
            'estimated_profit_usd': trade_amount * (profit_opportunity['net_profit_percentage'] / 100),
            'estimated_profit_percentage': profit_opportunity['net_profit_percentage']
        }

    def execute_arbitrage(self, opportunity, trade_amount):
        """Arbitraj işlemini uygula (SİMÜLASYON)"""
        logger.info(f"""
╔════════════════════════════════════════════════════╗
║        🚀 ARBİTRAJ İŞLEMİ BAŞLATILUYOR 🚀          ║
╚════════════════════════════════════════════════════╝
Token: {opportunity['base_token']}
Miktar: {trade_amount}$ USDT
Tahmini Kar: ${trade_amount['estimated_profit_usd']:.2f}
        """)
        
        # ⚠️ GÜVENLİ IŞLEM FLOWı (Gerçek işlemler için):
        # 1. Binance'de kısıtlı satın al
        # 2. PancakeSwap'ta satış
        # 3. Kar doğrula
        
        # Simülasyon sonucu
        simulated_profit = trade_amount['estimated_profit_usd'] * 0.95  # %5 slippage
        
        trade_record = {
            'timestamp': datetime.now(),
            'token': opportunity['base_token'],
            'amount_usdt': trade_amount['amount_usdt'],
            'estimated_profit': trade_amount['estimated_profit_usd'],
            'simulated_actual_profit': simulated_profit,
            'status': 'SIMULATED_SUCCESS'
        }
        
        self.trade_history.append(trade_record)
        self.total_profit += simulated_profit
        
        logger.info(f"✅ İşlem tamamlandı! Kar: ${simulated_profit:.2f}")
        return trade_record

    def get_performance_summary(self):
        """Performans özeti"""
        return {
            'total_trades': len(self.trade_history),
            'total_profit': self.total_profit,
            'average_profit_per_trade': self.total_profit / len(self.trade_history) if self.trade_history else 0,
            'trades': self.trade_history
        }
