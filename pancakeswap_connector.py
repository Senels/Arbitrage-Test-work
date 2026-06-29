import logging
from web3 import Web3
import json
import config

logger = logging.getLogger(__name__)

# PancakeSwap Router ABI
ROUTER_ABI = json.loads('''[
    {
        "inputs": [{"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                   {"internalType": "address[]", "name": "path", "type": "address[]"}],
        "name": "getAmountsOut",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "amountOut", "type": "uint256"},
                   {"internalType": "address[]", "name": "path", "type": "address[]"}],
        "name": "getAmountsIn",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    }
]''')

# ERC20 ABI (untuk token balance)
ERC20_ABI = json.loads('''[
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]''')

class PancakeSwapConnector:
    def __init__(self):
        try:
            self.w3 = Web3(Web3.HTTPProvider(config.PANCAKESWAP_RPC_URL))
            if self.w3.is_connected():
                logger.info("✅ BSC RPC bağlantısı başarılı")
            else:
                logger.error("❌ BSC RPC bağlantı başarısız")
                raise ConnectionError("Web3 bağlantısı kurulamadı")
            
            self.router_address = Web3.to_checksum_address(config.PANCAKESWAP_ROUTER)
            self.router_contract = self.w3.eth.contract(
                address=self.router_address,
                abi=ROUTER_ABI
            )
        except Exception as e:
            logger.error(f"❌ PancakeSwap başlatılamadı: {e}")
            raise

    def get_price(self, token_in, token_out, amount_in=1e18):
        """
        PancakeSwap'ta fiyat al
        token_in: Giriş token adresi
        token_out: Çıkış token adresi
        amount_in: İşlem miktarı (wei cinsinden)
        """
        try:
            token_in_checksum = Web3.to_checksum_address(token_in)
            token_out_checksum = Web3.to_checksum_address(token_out)
            
            amounts = self.router_contract.functions.getAmountsOut(
                int(amount_in),
                [token_in_checksum, token_out_checksum]
            ).call()
            
            price = amounts[1] / amount_in
            return price
        except Exception as e:
            logger.error(f"❌ PancakeSwap fiyatı alınamadı: {e}")
            return None

    def get_best_price_for_amount(self, token_in, token_out, amount):
        """Belirli miktar için en iyi fiyatı al"""
        try:
            token_in_checksum = Web3.to_checksum_address(token_in)
            token_out_checksum = Web3.to_checksum_address(token_out)
            
            amounts = self.router_contract.functions.getAmountsOut(
                int(amount),
                [token_in_checksum, token_out_checksum]
            ).call()
            
            return amounts[1]
        except Exception as e:
            logger.error(f"❌ İşlem tutarı hesaplanamadı: {e}")
            return None

    def get_token_balance(self, token_address, wallet_address):
        """Token bakiyesi al"""
        try:
            token_address = Web3.to_checksum_address(token_address)
            wallet_address = Web3.to_checksum_address(wallet_address)
            
            token_contract = self.w3.eth.contract(
                address=token_address,
                abi=ERC20_ABI
            )
            
            balance = token_contract.functions.balanceOf(wallet_address).call()
            decimals = token_contract.functions.decimals().call()
            
            return balance / (10 ** decimals)
        except Exception as e:
            logger.error(f"❌ Token bakiyesi alınamadı: {e}")
            return None

    def get_gas_price(self):
        """Güncel gas fiyatını al"""
        try:
            gas_price = self.w3.eth.gas_price
            return gas_price / 1e9  # Wei'den Gwei'ye çevir
        except Exception as e:
            logger.error(f"❌ Gas fiyatı alınamadı: {e}")
            return None

    def estimate_transaction_cost(self, gas_used=150000):
        """İşlem maliyetini tahmin et"""
        try:
            gas_price_gwei = self.get_gas_price()
            if not gas_price_gwei:
                return None
            
            gas_price_gwei *= config.GAS_PRICE_MULTIPLIER
            total_cost_usd = (gas_used * gas_price_gwei * 0.000000001) * 600  # BNB ≈ $600
            
            return {
                'gas_used': gas_used,
                'gas_price_gwei': gas_price_gwei,
                'total_cost_usd': total_cost_usd
            }
        except Exception as e:
            logger.error(f"❌ İşlem maliyeti tahmin edilemedi: {e}")
            return None
