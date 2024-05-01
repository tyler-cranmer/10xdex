from schema import ChainBase, Chain


class ChainDB:

    def __init__(self, db):
        self.db = db

    def insert(self, chain: ChainBase):
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO chain (chain_id, name, native_token, wrapped_token_address) VALUES (%s, %s, %s, %s) RETURNING id",
                (
                    chain.chain_id,
                    chain.name,
                    chain.native_token,
                    chain.wrapped_token_address,
                ),
            )
            chain_id = cur.fetchone()[0]
            self.db.commit()
            chain = Chain(id=chain_id, **chain.model_dump())
            return chain

    def get_all_chains(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM chain")
            return cur.fetchall()
            # return [Chain(**chain) for chain in cur.fetchall()]
