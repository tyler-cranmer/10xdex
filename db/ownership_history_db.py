import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from config import Settings
import logging

from schema import OwnershipHistory, OwnershipHistoryBase

logger = logging.getLogger(__name__)

s = Settings()


class OwnershipHistoryDB:
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

    def insert(self, ownership_history: OwnershipHistoryBase):
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO ownership_history (address, token_address, tx_hash, block_number, change, timestamp) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (
                        ownership_history.address,
                        ownership_history.token_address,
                        ownership_history.tx_hash,
                        ownership_history.block_number,
                        ownership_history.change,
                        ownership_history.timestamp,
                    ),
                )

                ownership_history_id = cur.fetchone()[0]
                conn.commit()
                return OwnershipHistory(
                    id=ownership_history_id, **ownership_history.model_dump()
                )
        except UniqueViolation as e:
            logger.error(
                f"Ownership history already exists: {ownership_history.address}.\nError: {e}"
            )
            raise ValueError(
                f"Ownership history already exists: {ownership_history.address}"
            )
        except Exception as e:
            raise ValueError(
                f"An error occurred while inserting the ownership history: {e}"
            )

    def get_all_ownership_history(self, address: str) -> list[OwnershipHistory]:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT id, address, token_address, tx_hash, block_number, change, timestamp FROM ownership_history WHERE address = %s",
                    (address,),
                )
                rows = cur.fetchall()
                if rows:
                    return [
                        OwnershipHistory(
                            id=row["id"],
                            address=row["address"],
                            token_address=row["token_address"],
                            tx_hash=row["tx_hash"],
                            block_number=row["block_number"],
                            change=row["change"],
                            timestamp=row["timestamp"],
                        )
                        for row in rows
                    ]
                else:
                    raise ValueError(
                        f"No ownership history found for address: {address}"
                    )
        except Exception as e:
            logger.error(f"An error occurred while getting all ownership history: {e}")
            return ValueError("An error occurred while getting all ownership history")
