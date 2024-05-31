import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from schema import (
    Wallet,
    WalletBase,
    WalletProtocolBalance,
    WalletProtocolBalanceBase,
    WalletToken,
    WalletTokenBase,
)
from config import Settings
import logging

logger = logging.getLogger(__name__)

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
            cursor_factory=DictCursor
        )

    def insert(self, wallet: WalletBase):
        """
        Insert a wallet into the database
        """
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO wallet (address, chain_id) VALUES (%s, %s) RETURNING id, created_at",
                    (
                        wallet.address,
                        wallet.chain_id,
                    ),
                )
                wallet_id, timestamp = cur.fetchone()
                conn.commit()
                return Wallet(id=wallet_id, created_at=timestamp, **wallet.model_dump())
        except UniqueViolation as e:
            logger.error(f"Wallet already exists: {wallet.address}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred while inserting the wallet: {e}")

    def insert_wallet_token_balance(self, wallet_token: WalletTokenBase):
        """
        Insert a wallet token balance into the database
        """
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO wallet_token_balance (wallet_id, token_id, balance) VALUES (%s, %s, %s) RETURNING id, time",
                    (
                        wallet_token.wallet_id,
                        wallet_token.token_id,
                        wallet_token.balance,
                    ),
                )
                wallet_token_balance_id, time = cur.fetchone()
                conn.commit()
                return WalletToken(id=wallet_token_balance_id, time=time, **wallet_token.model_dump())
        except UniqueViolation as e:
            logger.error(f"Wallet token balance already exists: {wallet_token.wallet_id} - {wallet_token.token_id}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred while inserting the wallet token balance: {e}")

    def insert_wallet_protocol_balance(self, wallet_protocol_balance: WalletProtocolBalanceBase):
        """
        Insert a wallet protocol balance into the database
        """
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO wallet_protocol_balance (wallet_id, protocol_dbank_id, net_usd_value, asset_usd_value, debt_usd_value) VALUES (%s, %s, %s, %s, %s) RETURNING id, time",
                    (
                        wallet_protocol_balance.wallet_id,
                        wallet_protocol_balance.protocol_dbank_id,
                        wallet_protocol_balance.net_usd_value,
                        wallet_protocol_balance.asset_usd_value,
                        wallet_protocol_balance.debt_usd_value,
                    ),
                )
                wallet_protocol_balance_id, time = cur.fetchone()
                conn.commit()
                return WalletProtocolBalance(
                    id=wallet_protocol_balance_id, time=time, **wallet_protocol_balance.model_dump()
                )
        except UniqueViolation as e:
            logger.error(f"Wallet protocol balance already exists: {wallet_protocol_balance.wallet_id} - {wallet_protocol_balance.protocol_dbank_id}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred while inserting the wallet protocol balance: {e}")
