import psycopg2
from schema import Transaction, TransactionBase
from config import Settings

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
        )


    def insert(self, transaction: TransactionBase):
        '''
        inserts a new transaction into the database
        '''
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO transaction (hash, chain_id, block_number, from_address, to_address, token_address, value) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
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
            transaction_id = cur.fetchone()[0]
            conn.commit()
            return Transaction(id=transaction_id, **transaction.model_dump())


