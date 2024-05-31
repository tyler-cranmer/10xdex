import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from config import Settings
from schema import PoolBase, Pool, PoolContract, PoolContractBase, PoolStats, PoolStatsBase, PoolWithContracts
import logging

s = Settings()
logger = logging.getLogger(__name__)

class PoolDB:
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


    def _insert_pool(self, pool: PoolBase):
        '''
        Insert a new pool into the database

        internal function
        '''
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO pool (dbank_id, protocol_dbank_id, name, controller) VALUES (%s, %s, %s, %s) RETURNING id, created_at",
                    (
                        pool.dbank_id,
                        pool.protocol_dbank_id,
                        pool.name,
                        pool.controller
                    ),
                )
                pool_id, timestamp = cur.fetchone()
                conn.commit()
                return Pool(id=pool_id, created_at=timestamp, **pool.model_dump())
        except UniqueViolation as e:
            logger.error(f"Pool already exists: {pool.dbank_id}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        
    def _insert_pool_contract(self, pool_contract: PoolContractBase):
        '''
        Insert a new pool contract into the database

        internal function
        '''
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO pool_contract (pool_dbank_id, address) VALUES (%s, %s) RETURNING id, created_at",
                    (
                        pool_contract.pool_dbank_id,
                        pool_contract.address,
                    ),
                )
                pool_contract_id, timestamp = cur.fetchone()
                conn.commit()
                return PoolContract(id=pool_contract_id, created_at=timestamp, **pool_contract.model_dump())
        except UniqueViolation as e:
            logger.error(f"Pool contract already exists: {pool_contract.address}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        

    def insert_pool_stats(self, pool_stats: PoolStatsBase):
        '''
        Insert a new pool stats into the database
        '''
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO pool_stats (pool_dbank_id, deposited_usd_value, deposited_user_count, deposited_valuable_user_count) VALUES (%s, %s, %s, %s) RETURNING id, time",
                    (
                        pool_stats.pool_dbank_id,
                        pool_stats.deposit_usd_value,
                        pool_stats.deposit_user_count,
                        pool_stats.deposit_valuable_user_count,
                    ),
                )
                pool_stats_id, timestamp = cur.fetchone()
                conn.commit()
                return PoolStats(id=pool_stats_id, time=timestamp, **pool_stats.model_dump())
        except UniqueViolation as e:
            logger.error(f"Pool stats already exist for: {pool_stats.pool_dbank_id}.\nError: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")


    def insert_pool_with_contracts(self, pool: PoolBase, contracts: list[PoolContractBase]):
        '''
        Combined insert for pool and contracts
        '''
        try:
            pool = self._insert_pool(pool)
            pool_with_contract = PoolWithContracts(pool=pool, contracts=[])
            for contract in contracts:
                c = self._insert_pool_contract(contract)
                pool_with_contract.contracts.append(c)
            return pool_with_contract
        except Exception as e:
            logger.error(f"An error occurred while inserting pool with contracts: {e}")

    def get_pool(self, dbank_id: str):
        '''
        retrieves the pool object using dbank_id
        '''
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT p.*, pc.*
                    FROM pool p
                    LEFT JOIN pool_contract pc ON p.dbank_id = pc.pool_dbank_id
                    WHERE p.dbank_id = %s
                    """,
                    (dbank_id,)
                )
                rows = cur.fetchall()
                if rows:
                    pool = Pool(
                        id=rows[0]['id'],
                        dbank_id=rows[0]['dbank_id'],
                        protocol_dbank_id=rows[0]['protocol_dbank_id'],
                        name=rows[0]['name'],
                        controller=rows[0]['controller'],
                        created_at=rows[0]['created_at'],
                    )
                    contracts = [PoolContract(id=row['id'], pool_dbank_id=row['pool_dbank_id'], address=row['address'], created_at=row['created_at']) for row in rows]
                    return PoolWithContracts(pool=pool, contracts=contracts)
                return None
        except Exception as e:
            logger.error(f"An error occurred while retrieving the pool: {e}")
            return None