import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from schema import ProtocolBase, Protocol
from config import Settings
import logging

logger = logging.getLogger(__name__)

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
            cursor_factory=DictCursor
        )

    def insert(self, protocol: ProtocolBase):
        '''
        Insert a new protocol into the database
        '''
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO protocol (chain_id, name, tvl, tvl_check, site_url, dbank_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, created_at",
                    (
                        protocol.chain_id,
                        protocol.name,
                        protocol.tvl,
                        protocol.tvl_check,
                        protocol.site_url,
                        protocol.dbank_id,
                    ),
                )
                protocol_id, created_at = cur.fetchone()
                conn.commit()
                return Protocol(id=protocol_id, created_at=created_at, **protocol.model_dump())
        except UniqueViolation as e:
            logger.error(f"Protocol already exists: {protocol.name}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred while inserting the protocol: {e}")

    def get_all_protocols(self):
        '''
        Retrieves all protocols from the database
        '''
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT id, chain_id, name, tvl, tvl_check, site_url, dbank_id, created_at FROM protocol"
                )
                rows = cur.fetchall()
                return [
                    Protocol(
                        id=row['id'],
                        chain_id=row['chain_id'],
                        name=row['name'],
                        tvl=row['tvl'],
                        tvl_check=row['tvl_check'],
                        site_url=row['site_url'],
                        dbank_id=row['dbank_id'],
                        created_at=row['created_at'],
                    )
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"An error occurred while retrieving protocols: {e}")
            return []
