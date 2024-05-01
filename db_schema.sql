CREATE TABLE chain (
    id SERIAL PRIMARY KEY NOT NULL,
    chain_id INT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    native_token TEXT NOT NULL,
    wrapped_token_address TEXT NOT NULL,
    dbank_id TEXT NOT NULL, 
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE token (
    id SERIAL PRIMARY KEY NOT NULL,
    chain_id INT NOT NULL,
    address TEXT NOT NULL,
    name TEXT NOT NULL,
    symbol TEXT NOT NULL,
    decimals INT NOT NULL,
    usd_value DOUBLE PRECISION NOT NULL,
    usd_check TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chain_id) REFERENCES chain(chain_id),
    UNIQUE (chain_id, address, name, symbol)
);

CREATE TABLE wallet (
    id SERIAL PRIMARY KEY NOT NULL,
    chain_id INT NOT NULL,
    address TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chain_id) REFERENCES chain(chain_id)
);

CREATE TABLE protocol (
    id SERIAL PRIMARY KEY NOT NULL,
    chain_id INT NOT NULL,
    name TEXT NOT NULL,
    tvl INT NOT NULL, 
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chain_id) REFERENCES chain(chain_id)
);

CREATE TABLE pool (
    id SERIAL PRIMARY KEY NOT NULL,
    pool_id TEXT NOT NULL UNIQUE,
    protocol_id INT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (protocol_id) REFERENCES protocol(id)
);

CREATE TABLE pool_contract (
    id SERIAL PRIMARY KEY NOT NULL,
    pool_id TEXT NOT NULL,
    address TEXT NOT NULL,
    FOREIGN KEY (pool_id) REFERENCES pool(pool_id)
);

-- HYPER TABLES --

CREATE TABLE wallet_token_balance (
    id SERIAL NOT NULL,
    wallet_id INT NOT NULL,
    token_id INT NOT NULL,
    balance DECIMAL(65, 18) NOT NULL,
    time TIMESTAMPTZ PRIMARY KEY NOT NULL,
    FOREIGN KEY (wallet_id) REFERENCES wallet(id),
    FOREIGN KEY (token_id) REFERENCES token(id)
);

SELECT create_hypertable('wallet_token_balance', by_range('time'));

CREATE INDEX token_id_idx ON wallet_token_balance (token_id, time DESC);
CREATE INDEX wallet_id_idx ON wallet_token_balance (wallet_id, time DESC);

CREATE TABLE txn_record (
    id SERIAL NOT NULL,
    chain_id INT NOT NULL,
    hash TEXT NOT NULL,
    block_number INT NOT NULL,
    from_address TEXT NOT NULL,
    to_address TEXT NOT NULL,
    token_address TEXT NOT NULL,
    amount DECIMAL(65, 18) NOT NULL,
    time TIMESTAMPTZ PRIMARY KEY NOT NULL,
    FOREIGN KEY (chain_id) REFERENCES chain(chain_id)
);

SELECT create_hypertable('txn_record', by_range('time'));

CREATE INDEX hash_idx ON public.txn_record (hash, time DESC);
CREATE INDEX block_number_idx ON txn_record (block_number, time DESC);
CREATE INDEX from_address_idx ON txn_record (from_address, time DESC);

CREATE TABLE pool_stats (
    id SERIAL NOT NULL,
    pool_id TEXT NOT NULL,
    deposited_usd_value DECIMAL(65, 18) NOT NULL,
    deposited_user_count INT NOT NULL,
    deposited_valable_user_count INT NOT NULL,
    time TIMESTAMPTZ PRIMARY KEY NOT NULL
);

SELECT create_hypertable('pool_stats', by_range('time'));

CREATE INDEX pool_stats_idx ON pool_stats (pool_id, time DESC);
