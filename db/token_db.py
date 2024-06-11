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
            cursor_factory=DictCursor,
        )

    def insert(self, token: TokenBase) -> Token:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tokens (address, name, symbol, decimal) VALUES (%s, %s, %s, %s) RETURNING id",
                    (token.address, token.name, token.symbol, token.decimal),
                )
                token_id = cur.fetchone()[0]
                conn.commit()
                return Token(id=token_id, **token.model_dump())
        except UniqueViolation as e:
            logger.error(f"Token already exists: {token.name}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred while inserting the token: {e}")

    def get_all_tokens(self) -> list[Token]:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute("SELECT id, address, name, symbol, decimal FROM tokens")
                rows = cur.fetchall()
                return [
                    Token(
                        id=row["id"],
                        address=row["address"],
                        name=row["name"],
                        symbol=row["symbol"],
                        decimal=row["decimal"],
                    )
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"An error occurred while getting all tokens: {e}")
            return []
        
    def get_token_by_address(self, address: str) -> Token:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT id, address, name, symbol, decimal FROM tokens WHERE address = %s",
                    (address,),
                )
                row = cur.fetchone()
                if row:
                    return Token(
                        id=row["id"],
                        address=row["address"],
                        name=row["name"],
                        symbol=row["symbol"],
                        decimal=row["decimal"],
                    )
                else: 
                    raise ValueError(f"Token with address {address} not found")
        except Exception as e:
            logger.error(f"An error occurred while getting token by address: {e}")
            raise ValueError("An error occurred while getting token by address") from e
    
    def get_token_by_name(self, name: str) -> Token | None:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT id, address, name, symbol, decimal FROM tokens WHERE name = %s",
                    (name,),
                )
                row = cur.fetchone()
                if row:
                    return Token(
                        id=row["id"],
                        address=row["address"],
                        name=row["name"],
                        symbol=row["symbol"],
                        decimal=row["decimal"],
                    )
                else:
                   raise ValueError(f"Token with name {name} not found")
        except Exception as e:
            logger.error(f"An error occurred while getting token by name: {e}")
            raise ValueError("An error occurred while getting token by address") from e