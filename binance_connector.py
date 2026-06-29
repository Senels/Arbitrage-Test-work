import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
import config

logger = logging.getLogger(__name__)

class BinanceConnector:
    def __init__(self):
        try:
            self.client = Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY)
            self.client.ping()
            logger.info("✅ Binance API bağlantısı başarılı")
        except BinanceAPIException as e:
            logger.error(f"❌ Binance API hatası: {e}")
            raise

    def get_price(self, symbol):
        """Binance'den gerçek zamanlı fiyat al"""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except BinanceAPIException as e:
            logger.error(f"❌ {symbol} fiyatı alınamadı: {e}")
            return None

    def get_multiple_prices(self, symbols):
        """Birden fazla symbol için fiyat al"""
        prices = {}
        for symbol in symbols:
            price = self.get_price(symbol)
            if price:
                prices[symbol] = price
        return prices

    def get_balance(self, asset):
        """Hesap bakiyesi kontrol et"""
        try:
            account = self.client.get_account()
            for balance in account['balances']:
                if balance['asset'] == asset:
                    return {
                        'free': float(balance['free']),
                        'locked': float(balance['locked']),
                        'total': float(balance['free']) + float(balance['locked'])
                    }
            return None
        except BinanceAPIException as e:
            logger.error(f"❌ Bakiye kontrol edilemedi: {e}")
            return None

    def get_order_book(self, symbol, limit=5):
        """Order book bilgisi al"""
        try:
            depth = self.client.get_order_book(symbol=symbol, limit=limit)
            return {
                'bids': [[float(price), float(quantity)] for price, quantity in depth['bids']],
                'asks': [[float(price), float(quantity)] for price, quantity in depth['asks']]
            }
        except BinanceAPIException as e:
            logger.error(f"❌ Order book alınamadı ({symbol}): {e}")
            return None

    def place_limit_order(self, symbol, side, quantity, price):
        """Limit order yerleştir"""
        try:
            order = self.client.order_limit(
                symbol=symbol,
                side=side,
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            logger.info(f"✅ Order yerleştirildi: {symbol} {side} {quantity} @ {price}")
            return order
        except BinanceAPIException as e:
            logger.error(f"❌ Order yerleştirilemedi: {e}")
            return None

    def place_market_order(self, symbol, side, quantity):
        """Market order yerleştir"""
        try:
            order = self.client.order_market(
                symbol=symbol,
                side=side,
                quantity=quantity
            )
            logger.info(f"✅ Market order yerleştirildi: {symbol} {side} {quantity}")
            return order
        except BinanceAPIException as e:
            logger.error(f"❌ Market order yerleştirilemedi: {e}")
            return None

    def cancel_order(self, symbol, order_id):
        """Order iptal et"""
        try:
            result = self.client.cancel_order(symbol=symbol, orderId=order_id)
            logger.info(f"✅ Order iptal edildi: {symbol} #{order_id}")
            return result
        except BinanceAPIException as e:
            logger.error(f"❌ Order iptal edilemedi: {e}")
            return None

    def get_trading_fees(self, symbol=None):
        """İşlem ücretlerini al"""
        try:
            if symbol:
                fees = self.client.get_trade_fee(symbol=symbol)
            else:
                fees = self.client.get_trade_fee()
            return fees
        except BinanceAPIException as e:
            logger.error(f"❌ Ücretler alınamadı: {e}")
            return None
