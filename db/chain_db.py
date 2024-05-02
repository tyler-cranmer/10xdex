import psycopg2
from schema import ChainBase, Chain
from config import Settings

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
        )

    def insert(self, chain: ChainBase):
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

    def get_chain_dbank_id(self, dbank_id):
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM chain WHERE dbank_id = %s", (dbank_id,))
            row = cur.fetchone()
            if row is None:
                return None
            return Chain(
                id=row[0],
                chain_id=row[1],
                name=row[2],
                native_token=row[3],
                wrapped_token_address=row[4],
                dbank_id=row[5],
                created_at=row[6],
            )

    def get_all_chains(self):
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT id, chain_id, name, native_token, wrapped_token_address, dbank_id, created_at FROM chain ORDER BY name ASC"
            )
            rows = cur.fetchall()
            return [
                Chain(
                    id=row[0],
                    chain_id=row[1],
                    name=row[2],
                    native_token=row[3],
                    wrapped_token_address=row[4],
                    dbank_id=row[5],
                    created_at=row[6],
                )
                for row in rows
            ]
