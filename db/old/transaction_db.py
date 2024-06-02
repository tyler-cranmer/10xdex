import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from db.old.schema_old import Transaction, TransactionBase
from config import Settings
import logging

logger = logging.getLogger(__name__)

s = Settings()

class TokenDB:
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

    def insert(self, transaction: TransactionBase):
        '''
        inserts a new transaction into the database
        '''
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO transaction (hash, chain_id, block_number, from_address, to_address, token_address, value) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id, created_at",
                    (
                        transaction.hash,
                        transaction.chain_id,
                        transaction.block_number,
                        transaction.from_address,
                        transaction.to_address,
                        transaction.token_address,
                        transaction.value
                    ),
                )
                transaction_id, timestamp = cur.fetchone()
                conn.commit()
                return Transaction(id=transaction_id, created_at=timestamp, **transaction.model_dump())
        except UniqueViolation as e:
            logger.error(f"Transaction already exists: {transaction.hash}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred while inserting the transaction: {e}")

