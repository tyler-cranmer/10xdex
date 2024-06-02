import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation

from config import Settings
import logging

from schema import WalletBase, Wallet

logger = logging.getLogger(__name__)

s = Settings()

class WalletDB:
    def __init__(self):
        self.settings = s

    def _connect(self) -> psycopg2.extensions.connection:
        return psycopg2.connect(
            host=self.settings.POSTGRES_HOST,
            user=self.settings.POSTGRES_USER,
            password=self.settings.POSTGRES_PASSWORD,
            dbname=self.settings.POSTGRES_DB,
            cursor_factory=DictCursor
        )

    def insert(self, wallet: WalletBase) -> Wallet:
        """
        Insert a wallet into the database
        """
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO wallet (address, first_seen, last_seen, total_recieved, total_sent) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (
                        wallet.address,
                        wallet.first_seen, 
                        wallet.last_seen,
                        wallet.total_received,
                        wallet.total_sent,
                    ),
                )
                id = cur.fetchone()
                conn.commit()
                return Wallet(id=id, **wallet.model_dump())
            
        except UniqueViolation as e:
            logger.error(f"Wallet already exists: {wallet.address}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred while inserting the wallet: {e}")


    def update(self, address: str, last_seen=None, total_received=None, total_sent=None) -> Wallet:
        """
        Update a wallet in the database
        """
        try:
            with self._connect() as conn, conn.cursor() as cur:
                # Start with the base update query
                query = "UPDATE wallet SET"
                data = []
                params = []

                # Conditionally add other fields to the query
                if last_seen is not None:
                    params.append(" last_seen = %s")
                    data.append(last_seen)
                if total_received is not None:
                    params.append(" total_received = %s")
                    data.append(total_received)
                if total_sent is not None:
                    params.append(" total_sent = %s")
                    data.append(total_sent)

                if not params:
                    raise ValueError("No fields to update.")

                query += ",".join(params)
                query += " WHERE address = %s"
                data.append(address)

                cur.execute(query, tuple(data))
                conn.commit()
                
                cur.execute("SELECT * FROM wallet WHERE address = %s", (address,))
                updated_record = cur.fetchone()

                return Wallet(**updated_record)
        except Exception as e:
            logger.error(f"An error occurred while updating the wallet: {e}")
