from binance.spot import Spot
import config

class BinanceConnector:
    def __init__(self):
        self.client = Spot(api_key=config.BINANCE_API_KEY,
                           api_secret=config.BINANCE_SECRET_KEY)
        try:
            self.client.ping()
            print("✅ Binance mainnet bağlantısı başarılı")
        except Exception as e:
            print("❌ Binance bağlantı hatası:", e)
