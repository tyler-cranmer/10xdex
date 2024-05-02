import psycopg2
from schema import Wallet, WalletBase, WalletProtocolBalance, WalletProtocolBalanceBase, WalletToken, WalletTokenBase
from config import Settings

s = Settings()

class WalletDB:
    def __init__(self):
        self.settings = s

    def _connect(self):
        return psycopg2.connect(
            host=self.settings.POSTGRES_HOST,
            user=self.settings.POSTGRES_USER,
            password=self.settings.POSTGRES_PASSWORD,
            dbname=self.settings.POSTGRES_DB,
        )
    
    def insert(self, wallet: WalletBase):
        """ 
        Insert a wallet into the database
        """
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO wallet (address, chain_id) VALUES (%s, %s) RETURNING id",
                (
                    wallet.address,
                    wallet.chain_id,
                ),
            )
            wallet_id = cur.fetchone()[0]
            conn.commit()
            return Wallet(id=wallet_id, **wallet.model_dump())
        
    def insert_wallet_token_balance(self, wallet: WalletTokenBase):
        '''
        Insert a wallet token balance into the database
        '''
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO wallet_token_balance (wallet_id, token_id, balance) VALUES (%s, %s, %s) RETURNING id",
                (
                    wallet.wallet_id,
                    wallet.token_id,
                    wallet.balance,
                ),
            )
            wallet_token_balance_id = cur.fetchone()[0]
            conn.commit()
            return WalletToken(id=wallet_token_balance_id, **wallet.model_dump())
        

    def insert_wallet_protocol_balance(self, wallet: WalletProtocolBalanceBase):
        '''
        Insert a wallet protocol balance into the database
        '''
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO wallet_protocol_balance (wallet_id, protocol_dbank_id, net_usd_value, asset_usd_value, debt_usd_value ) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (
                    wallet.wallet_id,
                    wallet.protocol_dbank_id,
                    wallet.net_usd_value,
                    wallet.asset_usd_value,
                    wallet.debt_usd_value
                ),
            )
            wallet_protocol_balance_id = cur.fetchone()[0]
            conn.commit()
            return WalletProtocolBalance(id=wallet_protocol_balance_id, **wallet.model_dump())