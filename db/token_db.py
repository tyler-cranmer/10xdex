import psycopg2
from schema import TokenBase, Token
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

    def insert(self, token: TokenBase):
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

    def get_all_tokens(self):
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT id, address, name, chain_id, symbol, decimals, usd_value, usd_check, created_at FROM token"
            )
            rows = cur.fetchall()
            return [
                Token(
                    id=row[0],
                    address=row[1],
                    name=row[2],
                    symbol=row[3],
                    decimals=row[4],
                    chain_id=row[5],
                    usd_value=row[6],
                    usd_check=row[7],
                    created_at=row[8],
                )
                for row in rows
            ]
