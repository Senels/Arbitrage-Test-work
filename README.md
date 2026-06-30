# 🤖 Kripto Arbitraj Bot - En Karlı Konfigürasyon

Binance (CEX) ve PancakeSwap (DEX) arasında otomatik arbitraj işlemleri yapan bot.

## 🎯 Strateji

- **Blockchain**: BSC (Binance Smart Chain) - Düşük gaz ücretleri
- **DEX**: PancakeSwap - Yüksek likidite
- **CEX**: Binance - Spot trading
- **Minimum Kar Eşiği**: %0.5
- **İşlem Aralığı**: Her 5 saniye

## 💡 Arbitraj Akışı

```
Binance (Ucuz Fiyat)
        ↓
     AL (BNB)
        ↓
PancakeSwap (Pahalı Fiyat)
        ↓
     SAT (USDT)
        ↓
    KAR ✅
```

## 📦 Kurulum

### Gereksinimler
- Python 3.8+
- Binance API anahtarları
- BSC RPC erişimi

### Adımlar

1. **Repository'yi klonla**
```bash
git clone https://github.com/Senels/Arbitrage-Test-work.git
cd Arbitrage-Test-work
```

2. **Branch'i checkout et**
```bash
git checkout arbitrage-bot-main
```

3. **Dependencies'i yükle**
```bash
pip install -r requirements.txt
```

4. **.env dosyasını oluştur**
```bash
cp .env.example .env
```

5. **.env dosyasını düzenle**
```
BINANCE_API_KEY=your_key_here
BINANCE_SECRET_KEY=your_secret_here
```

6. **Bot'u çalıştır**
```bash
python main.py
```

## 📊 Desteklenen Token'lar

| Token | Volatilite | Likidite | Tercih |
|-------|-----------|----------|--------|
| USDT  | Çok Düşük | Çok Yüksek | ⭐⭐⭐⭐⭐ |
| BUSD  | Çok Düşük | Yüksek | ⭐⭐⭐⭐ |
| USDC  | Çok Düşük | Yüksek | ⭐⭐⭐⭐ |
| BNB   | Düşük | Çok Yüksek | ⭐⭐⭐⭐⭐ |
| ETH   | Düşük | Çok Yüksek | ⭐⭐⭐⭐⭐ |
| BTC   | Orta | Çok Yüksek | ⭐⭐⭐⭐ |

## ⚙️ Konfigürasyon

`config.py` dosyasında ayarlar bulunur:

```python
PROFIT_THRESHOLD = 0.005  # 0.5% minimum kar
MIN_USDT_AMOUNT = 100     # Minimum işlem miktarı
MAX_SLIPPAGE = 0.02       # 2% max slippage
CHECK_INTERVAL = 5        # 5 saniye kontrol aralığı
```

## 🔧 Modüller

### `binance_connector.py`
Binance API entegrasyonu
- Gerçek zamanlı fiyat al
- Bakiye kontrol
- Order yönetimi

### `pancakeswap_connector.py`
PancakeSwap Web3 entegrasyonu
- DEX fiyatları
- Token bakiyesi
- Gaz tahminleri

### `arbitrage_engine.py`
Arbitraj motoru
- Fırsat tespiti
- Kar hesaplama
- İşlem yönetimi

### `main.py`
Bot orkestrasyonu
- Zamanlayıcı
- Monitör
- Performans

## ⚠️ RİSK UYARISI

1. **Gerçek API Anahtarları**: Asla production API anahtarlarını paylaşmayın
2. **Gaz Ücretleri**: BSC ücretsiz değildir, işlem maliyetlerini hesapla
3. **Slippage**: Fiyat farkları işlem sırasında değişebilir
4. **Likidite Riski**: Büyük işlemler için yeterli likidite kontrol et
5. **Kaldıraç Yok**: Bu bot spot işlemleri yapıyor

## 📈 Kar Potansiyeli

- **Aylık Hedef**: %2-5 (Minimum 100$)
- **Saatlik Kontrol**: Her 5 saniyede
- **Günlük İşlem**: 10-50 arası
- **Başabaş Noktası**: %0.5-1 kar

## 🚀 İleri Özellikler (Gelecek)

- [ ] Multiple exchange arbitrajı
- [ ] DEX havuz taraması
- [ ] Risk yönetimi algoritmaları
- [ ] Telegram bildirimleri
- [ ] Dashboard UI
- [ ] Veritabanı kaydı

## 📝 Logs

Bot çalışırken loglama ile durum izlenebilir:

```
✅ Binance API bağlantısı başarılı
✅ BSC RPC bağlantısı başarılı
💰 KARLII ARBİTRAJ FIRSATI 💰
   Token: BNB
   NET KAR: 0.6234%
🚀 ARBİTRAJ İŞLEMİ BAŞLATILUYOR 🚀
✅ İşlem tamamlandı! Kar: $0.62
```

## 🤝 Katkıda Bulunma

Görüş ve öneriler için Issue veya Pull Request açın.

## 📄 Lisans

MIT License

---

**⚡ En Karlı Konfigürasyon ile Hazır - Hemen Çalıştırın!**
