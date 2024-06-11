import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from config import Settings
import logging

from schema import PriceDataBase, PriceData

logger = logging.getLogger(__name__)

s = Settings()






class PriceDataDB:
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
    
    def insert(self, price_data: PriceDataBase) -> PriceData:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO price_data (token_address, price, timestamp) VALUES (%s, %s, %s) RETURNING id",
                    (
                        price_data.token_address,
                        price_data.price,
                        price_data.timestamp,
                    ),
                )

                price_data_id = cur.fetchone()[0]
                conn.commit()
                return PriceData(
                    id=price_data_id, **price_data.model_dump()
                )
        except UniqueViolation as e:
            logger.error(
                f"Price Data already exists: {price_data.token_address}.\nError: {e}"
            )
            raise ValueError(
                f"Price Data already exists: {price_data.token_address}"
            )
        except Exception as e:
            logger.error(f"An error occurred while inserting the price data: {e}")
            raise ValueError(
                f"An error occurred while inserting the price data: {e}"
            )