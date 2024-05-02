
import psycopg2
from schema import ProtocolBase, Protocol
from config import Settings

s = Settings()


class ProtocolDB:

    def __init__(self):
        self.settings = s

    def _connect(self):
        return psycopg2.connect(
            host=self.settings.POSTGRES_HOST,
            user=self.settings.POSTGRES_USER,
            password=self.settings.POSTGRES_PASSWORD,
            dbname=self.settings.POSTGRES_DB,
        )
    
    def insert(self, protocol: ProtocolBase):
        '''
        Insert a new protocol into the database
        '''
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO protocol (chain_id, name, tvl, tvl_check, site_url, dbank_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (
                    protocol.chain_id,
                    protocol.name,
                    protocol.tvl,
                    protocol.tvl_check,
                    protocol.site_url,
                    protocol.dbank_id,
                ),
            )
            protocol_id = cur.fetchone()[0]
            conn.commit()
            return Protocol(id=protocol_id, **protocol.model_dump())
        
    def get_all_protocols(self):
        '''
        Retrieves all protocols from the database
        '''
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT id, chain_id, name, tvl, tvl_check, site_url, dbank_url, created_at FROM protocol"
            )
            rows = cur.fetchall()
            return [
                Protocol(
                    id=row[0],
                    chain_id=row[1],
                    name=row[2],
                    tvl=row[3],
                    tvl_check=row[4],
                    site_url=row[5],
                    dbank_url=row[6],
                    created_at=row[7],
                )
                for row in rows
            ]