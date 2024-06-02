import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from db.old.schema_old import ChainBase, Chain
from config import Settings
import logging

logger = logging.getLogger(__name__)

s = Settings()

class ChainDB:
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

    def insert(self, chain: ChainBase):
        '''
        Insert a new chain into the database
        '''
        conn = None
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO chain (chain_id, name, native_token, wrapped_token_address, dbank_id) VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at",
                    (
                        chain.chain_id,
                        chain.name,
                        chain.native_token,
                        chain.wrapped_token_address,
                        chain.dbank_id,
                    ),
                )
                chain_id, timestamp = cur.fetchone()
                conn.commit()
                return Chain(id=chain_id, created_at=timestamp, **chain.model_dump())
        
        except UniqueViolation as e:
            if conn:
                conn.rollback()
            logger.error(f"Chain already exists: {chain.name}.\nError: {e}")

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"An error occurred: {e}")

    def get_chain_dbank_id(self, dbank_id):
        '''
        Retrieves a chain object from the database using the dbank_id
        '''
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM chain WHERE dbank_id = %s", (dbank_id,))
            row = cur.fetchone()
            if row is None:
                return None
            return Chain(
                id=row['id'],
                chain_id=row['chain_id'],
                name=row['name'],
                native_token=row['native_token'],
                wrapped_token_address=row['wrapped_token_address'],
                dbank_id=row['dbank_id'],
                created_at=row['created_at'],
            )

    def get_all_chains(self):
        '''
        Retrieves all chains from the database
        '''
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT id, chain_id, name, native_token, wrapped_token_address, dbank_id, created_at FROM chain ORDER BY name ASC"
            )
            rows = cur.fetchall()
            return [
                Chain(
                    id=row['id'],
                    chain_id=row['chain_id'],
                    name=row['name'],
                    native_token=row['native_token'],
                    wrapped_token_address=row['wrapped_token_address'],
                    dbank_id=row['dbank_id'],
                    created_at=row['created_at'],
                )
                for row in rows
            ]
