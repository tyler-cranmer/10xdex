
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from config import Settings
import logging

from schema import TransactionBase, Transaction

logger = logging.getLogger(__name__)

s = Settings()





class TransactionDB:
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
    def insert(self, transaction: TransactionBase) -> Transaction:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO transactions (tx_hash, block_number, from_address, to_address, value, timestamp) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (
                        transaction.tx_hash,
                        transaction.block_number,
                        transaction.from_address,
                        transaction.to_address,
                        transaction.value,
                        transaction.timestamp,
                    ),
                )

                transaction_id = cur.fetchone()[0]
                conn.commit()
                return Transaction(
                    id=transaction_id, **transaction.model_dump()
                )
        except UniqueViolation as e:
            logger.error(
                f"Transaction already exists: {transaction.tx_hash}.\nError: {e}"
            )
            raise ValueError(
                f"Transaction already exists: {transaction.tx_hash}"
            )
        
    def get_transaction(self, tx_hash: str) -> Transaction:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT id, tx_hash, block_number, from_address, to_address, value, timestamp FROM transactions WHERE tx_hash = %s",
                    (tx_hash,),
                )
                row = cur.fetchone()
                if row:
                    return Transaction(
                        id=row["id"],
                        tx_hash=row["tx_hash"],
                        block_number=row["block_number"],
                        from_address=row["from_address"],
                        to_address=row["to_address"],
                        value=row["value"],
                        timestamp=row["timestamp"],
                    )
                return None
        except Exception as e:
            logger.error(f"An error occurred while getting the transaction: {e}")
            return None
