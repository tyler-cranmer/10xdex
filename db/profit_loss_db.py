import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from config import Settings
import logging

from schema import ProfitLossBase, ProfitLoss

logger = logging.getLogger(__name__)

s = Settings()


class ProfitLossDB:
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
    
    def insert(self, profit_loss: ProfitLossBase) -> ProfitLoss:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO profit_loss (wallet_address, token_address, profit_loss, timestamp) VALUES (%s, %s, %s, %s) RETURNING id",
                    (
                        profit_loss.wallet_address,
                        profit_loss.token_address,
                        profit_loss.profit_loss,
                        profit_loss.timestamp,
                    ),
                )

                profit_loss_id = cur.fetchone()[0]
                conn.commit()
                return ProfitLoss(
                    id=profit_loss_id, **profit_loss.model_dump()
                )
        except UniqueViolation as e:
            logger.error(
                f"Profit Loss already exists: {profit_loss.wallet_address}.\nError: {e}"
            )
            raise ValueError(
                f"Profit Loss already exists: {profit_loss.wallet_address}"
            )
    
