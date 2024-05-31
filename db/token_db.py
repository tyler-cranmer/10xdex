import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from schema import TokenBase, Token
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

    def insert(self, token: TokenBase):
        '''
        Insert a new token into the database
        '''
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO token (address, name, symbol, decimals, chain_id, usd_value, usd_check) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id, created_at",
                    (
                        token.address,
                        token.name,
                        token.symbol,
                        token.decimals,
                        token.chain_id,
                        token.usd_value,
                        token.usd_check,
                    ),
                )
                token_id, timestamp = cur.fetchone()
                conn.commit()
                return Token(id=token_id, created_at=timestamp, **token.model_dump())
        except UniqueViolation as e:
            logger.error(f"Token already exists: {token.name}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred while inserting the token: {e}")

    def get_all_tokens(self):
        '''
        Gets all tokens from the database
        '''
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT id, address, name, chain_id, symbol, decimals, usd_value, usd_check, created_at FROM token"
                )
                rows = cur.fetchall()
                return [
                    Token(
                        id=row['id'],
                        address=row['address'],
                        name=row['name'],
                        symbol=row['symbol'],
                        decimals=row['decimals'],
                        chain_id=row['chain_id'],
                        usd_value=row['usd_value'],
                        usd_check=row['usd_check'],
                        created_at=row['created_at'],
                    )
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"An error occurred while retrieving tokens: {e}")
            return []
