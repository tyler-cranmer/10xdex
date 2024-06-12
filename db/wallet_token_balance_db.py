
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from config import Settings
import logging

from schema import WalletTokenBalance, WalletTokenBalanceBase

logger = logging.getLogger(__name__)

s = Settings()



class WalletTokenBalanceDB:
    def __init__(self):
        self.settings = s

    def _connect(self):
        return psycopg2.connect(
            host=self.settings.POSTGRES_HOST,
            user=self.settings.POSTGRES_USER,
            password=self.settings.POSTGRES_PASSWORD,
            dbname=self.settings.POSTGRES_DB,
            cursor_factory=DictCursor,
        )


    def insert(self, wallet_token_balance: WalletTokenBalanceBase) -> WalletTokenBalance:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO wallet_token_balance (wallet_id, token_id, balance, timestamp) VALUES (%s, %s, %s, %s) RETURNING id",
                    (
                        wallet_token_balance.wallet_id,
                        wallet_token_balance.token_id,
                        wallet_token_balance.balance,
                        wallet_token_balance.timestamp,
                    ),
                )

                wallet_token_balance_id = cur.fetchone()[0]
                conn.commit()
                return WalletTokenBalance(
                    id=wallet_token_balance_id, **wallet_token_balance.model_dump()
                )
        except UniqueViolation as e:
            logger.error(
                f"Wallet token balance already exists: {wallet_token_balance.wallet_id}.\nError: {e}"
            )
            raise ValueError(
                f"Wallet token balance already exists: {wallet_token_balance.wallet_id}"
            )

    def get_wallet_token_balance(self, address: str) -> list[WalletTokenBalance]:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT id, wallet_id, token_id, balance, timestamp FROM wallet_token_balance WHERE wallet_id = %s",
                    (address,),
                )
                rows = cur.fetchall()
                if rows:
                    return [
                        WalletTokenBalance(
                            id=row["id"],
                            wallet_id=row["wallet_id"],
                            token_id=row["token_id"],
                            balance=row["balance"],
                            timestamp=row["timestamp"],
                        )
                        for row in rows
                    ]
                else: 
                    raise ValueError(f"Wallet token balance not found: {address}")
        except Exception as e:
            logger.error(f"An error occurred while getting wallet token balance: {e}")
            raise ValueError(f"An error occurred while getting wallet token balance: {e}")