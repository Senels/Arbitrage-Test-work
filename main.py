#!/usr/bin/env python3
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from arbitrage_engine import ArbitrageEngine
import config

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ArbitrageBot:
    def __init__(self):
        logger.info("🤖 Arbitraj Bot başlatılıyor...")
        self.engine = ArbitrageEngine()
        self.scheduler = BackgroundScheduler()
        self.is_running = False

    def monitor_and_trade(self):
        """Fırsatları izle ve arbitraj işlemlerini yap"""
        try:
            # Tüm çiftleri tara
            opportunities = self.engine.scan_all_pairs()
            
            if not opportunities:
                return
            
            # Kârlı fırsatları bul
            profitable_opportunities = [
                opp for opp in opportunities 
                if opp['is_profitable']
            ]
            
            if profitable_opportunities:
                logger.warning(f"🎯 {len(profitable_opportunities)} kârlı fırsat bulundu!")
                
                # İlk kârlı fırsatı işle (risk yönetimi)
                best_opportunity = max(
                    profitable_opportunities,
                    key=lambda x: x['net_profit_percentage']
                )
                
                # İşlem miktarını hesapla
                trade_calc = self.engine.calculate_trade_amount(
                    best_opportunity,
                    available_usdt=500  # Simülasyon için sabit miktar
                )
                
                if trade_calc:
                    # Arbitraj işlemini uygula
                    self.engine.execute_arbitrage(best_opportunity, trade_calc)
        
        except Exception as e:
            logger.error(f"❌ Monitör hatası: {e}")

    def start(self):
        """Bot'u başlat"""
        logger.info("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        🚀 KRİPTO ARBITRAJ BOT - EN KARLII KONFİG 🚀           ║
║                                                               ║
║  Strateji: Binance ↔ PancakeSwap Arbitrajı                    ║
║  Blockchain: BSC (Binance Smart Chain)                        ║
║  Minimum Kar Eşiği: %0.5                                      ║
║  İşlem Aralığı: Her 5 saniye                                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        
        self.is_running = True
        
        # Scheduler'ı ayarla
        self.scheduler.add_job(
            self.monitor_and_trade,
            'interval',
            seconds=config.CHECK_INTERVAL,
            id='arbitrage_monitor'
        )
        
        self.scheduler.start()
        logger.info("✅ Bot çalışıyor...")
        
        # Botu çalıştırmaya devam et
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Bot'u durdur"""
        logger.info("⏹️ Bot durduruluyor...")
        self.is_running = False
        self.scheduler.shutdown()
        
        # Performans özeti
        summary = self.engine.get_performance_summary()
        logger.info(f"""
╔═══════════════════════════════════════════════════════════════╗
║                   📊 PERFORMANS ÖZETİ 📊                      ║
╚═══════════════════════════════════════════════════════════════╝
Toplam İşlem: {summary['total_trades']}
Toplam Kar: ${summary['total_profit']:.2f}
Ortalama İşlem Kar: ${summary['average_profit_per_trade']:.2f}
        """)

if __name__ == "__main__":
    bot = ArbitrageBot()
    bot.start()
