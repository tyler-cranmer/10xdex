

from contextvars import Token
from schema import TokenBase


class TokenDB:
    def __init__(self, db):
        self.db = db

    def insert(self, token: TokenBase):
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO token (address, name, symbol, decimals, chain_id, usd_value, usd_check) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
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
            token_id = cur.fetchone()[0]
            self.db.commit()
            token = Token(id=token_id, **token.model_dump())
            return token