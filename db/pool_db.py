import psycopg2
from config import Settings
from schema import PoolBase, Pool, PoolContract, PoolContractBase, PoolStats, PoolStatsBase, PoolWithContracts

s = Settings()


class PoolDB:
    def __init__(self):
        self.settings = s

    def _connect(self):
        return psycopg2.connect(
            host=self.settings.POSTGRES_HOST,
            user=self.settings.POSTGRES_USER,
            password=self.settings.POSTGRES_PASSWORD,
            dbname=self.settings.POSTGRES_DB,
        )


    def _insert_pool(self, pool: PoolBase):
        '''
        Insert a new pool into the database

        internal function
        '''
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO pool (dbank_id, protocol_dbank_id, name, controller) VALUES (%s, %s, %s) RETURNING id, created_at",
                (
                    pool.dbank_id,
                    pool.protocol_dbank_id,
                    pool.name,
                    pool.controller
                ),
            )
            pool_id, timestamp = cur.fetchone()[0]
            conn.commit()
            return Pool(id=pool_id, created_at= timestamp, **pool.model_dump())
        
    def _insert_pool_contract(self, pool_contract: PoolContractBase):
        '''
        Insert a new pool contract into the database

        internal function
        '''
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
        

    def insert_pool_stats(self, pool_stats: PoolStatsBase):
        '''
        Insert a new pool stats into the database
        '''
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO pool_stats (pool_dbank_id, deposited_usd_value, deposit_user_count, deposit_valuable_user_count) VALUES (%s, %s, %s, %s) RETURNING id, time",
                (
                    pool_stats.pool_dbank_id,
                    pool_stats.deposited_usd_value,
                    pool_stats.deposit_user_count,
                    pool_stats.deposit_valuable_user_count,
                ),
            )
            pool_stats_id, timestamp = cur.fetchone()
            conn.commit()
            return PoolStats(id=pool_stats_id, time=timestamp, **pool_stats.model_dump())


    def insert_pool_with_contracts(self, pool: PoolBase, contracts: list[PoolContractBase]):
        '''
        Combined insert for pool and contracts
        '''
        pool = self._insert_pool(pool)
        pool_with_contract = PoolWithContracts(pool=pool, contracts=[])
        for contract in contracts:
            c = self._insert_pool_contract(contract)
            pool_with_contract.contracts.append(c)
        return pool_with_contract

    def get_pool(self, dbank_id: str):
        '''
        retrieves the pool object using p
        '''
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.*, pc.*
                FROM pool p
                LEFT JOIN pool_contract pc ON p.id = pc.protocol_dbank_id
                WHERE p.dbank_id = %s
                """,
                (dbank_id)
            )
            rows = cur.fetchall()
            if rows:
                pool = Pool(
                    id=rows[0][0],
                    pool_dbank_id=rows[0][1],
                    protocol_dbank_id=rows[0][2],
                    name=rows[0][3],
                    controller=rows[0][4],
                    created_at=rows[0][5],
                )
                contracts = [PoolContract(id=row[6], pool_id=row[7], address=row[8], created_at=row[9]) for row in rows]
                return PoolWithContracts(pool=pool, contracts=contracts)