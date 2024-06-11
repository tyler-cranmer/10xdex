
--  NEW DB SCHEMA --

CREATE EXTENSION IF NOT EXISTS timescaleDB;

CREATE TABLE wallets (
    id SERIAL PRIMARY KEY,
    address TEXT NOT NULL UNIQUE,
    first_seen TIMESTAMPTZ,
    last_seen TIMESTAMPTZ,
    total_received NUMERIC DEFAULT 0,
    total_sent NUMERIC DEFAULT 0
);

CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    address TEXT NOT NULL UNIQUE,
    name TEXT,
    symbol TEXT,
    decimal INT,
);

CREATE TABLE ownership_history (
    id SERIAL PRIMARY KEY,
    address TEXT NOT NULL,
    token_address TEXT NOT NULL,
    tx_hash TEXT NOT NULL,
    block_number INT NOT NULL,
    change NUMERIC NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
SELECT create_hypertable('ownership_history', 'timestamp');

CREATE TABLE wallet_token_balance (
    id SERIAL PRIMARY KEY,
    wallet_id INT NOT NULL,
    token_id INT NOT NULL,
    balance DECIMAL(30,0) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    FOREIGN KEY (wallet_id) REFERENCES wallets(id),
    FOREIGN KEY (token_id) REFERENCES tokens(id),
    UNIQUE (wallet_id, token_id, time)
);

SELECT create_hypertable('wallet_token_balance', 'timestamp');

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    tx_hash TEXT NOT NULL UNIQUE,
    block_number INT NOT NULL,
    from_address TEXT,
    to_address TEXT,
    token_address TEXT,
    value NUMERIC,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
SELECT create_hypertable('transactions', 'timestamp');

CREATE TABLE profit_loss (
    id SERIAL PRIMARY KEY,
    wallet_address INT NOT NULL,
    token_address INT NOT NULL,
    profit_loss NUMERIC NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,  -- Use timestamp to track changes over time
    FOREIGN KEY (wallet_address) REFERENCES wallets(address),
    FOREIGN KEY (token_address) REFERENCES tokens(address),
    UNIQUE (wallet_address, token_address, timestamp)
);

SELECT create_hypertable('profit_loss', 'timestamp');

CREATE TABLE price_data (
    id SERIAL PRIMARY KEY,
    token_address TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    price NUMERIC NOT NULL,
    UNIQUE(token_address, timestamp)
);

SELECT create_hypertable('price_data', 'timestamp');




-- CREATE TABLE chain (
--     id SERIAL PRIMARY KEY NOT NULL,
--     chain_id INT NOT NULL UNIQUE,
--     name TEXT NOT NULL,
--     native_token TEXT NOT NULL,
--     wrapped_token_address TEXT NOT NULL,
--     dbank_id TEXT NOT NULL UNIQUE, 
--     created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE TABLE token (
--     id SERIAL PRIMARY KEY NOT NULL,
--     chain_id INT NOT NULL,
--     address TEXT NOT NULL,
--     name TEXT NOT NULL,
--     symbol TEXT NOT NULL,
--     decimals INT NOT NULL,
--     usd_value DECIMAL(20,5) NOT NULL,
--     usd_check TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (chain_id) REFERENCES chain(chain_id),
--     UNIQUE (chain_id, address, name, symbol)
-- );

-- CREATE TABLE wallet (
--     id SERIAL PRIMARY KEY NOT NULL,
--     chain_id INT NOT NULL,
--     address TEXT NOT NULL,
--     private_key TEXT NULL,
--     created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (chain_id) REFERENCES chain(chain_id),
--     UNIQUE (chain_id, address)
-- );

-- CREATE TABLE protocol (
--     id SERIAL PRIMARY KEY NOT NULL,
--     chain_id INT NOT NULL,
--     name TEXT NOT NULL,
--     tvl DECIMAL(20,5) NOT NULL, 
--     tvl_check TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     site_url TEXT NOT NULL,
--     dbank_id TEXT NOT NULL UNIQUE,
--     created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (chain_id) REFERENCES chain(chain_id)
-- );

-- CREATE TABLE pool (
--     id SERIAL PRIMARY KEY NOT NULL,
--     dbank_id TEXT NOT NULL UNIQUE,
--     protocol_dbank_id TEXT NOT NULL,
--     name TEXT NOT NULL,
--     controller TEXT NOT NULL,
--     created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (protocol_dbank_id) REFERENCES protocol(dbank_id)
-- );

-- CREATE TABLE pool_contract (
--     id SERIAL PRIMARY KEY NOT NULL,
--     pool_dbank_id TEXT NOT NULL,
--     address TEXT NOT NULL,
--     created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (pool_dbank_id) REFERENCES pool(dbank_id)
-- );


-- -- HYPER TABLES --

-- CREATE TABLE wallet_token_balance (
--     id SERIAL NOT NULL,
--     wallet_id INT NOT NULL,
--     token_id INT NOT NULL,
--     balance DECIMAL(30,0) NOT NULL,
--     time TIMESTAMPTZ PRIMARY KEY NOT NULL,
--     FOREIGN KEY (wallet_id) REFERENCES wallet(id),
--     FOREIGN KEY (token_id) REFERENCES token(id)
-- );

-- SELECT create_hypertable('wallet_token_balance', by_range('time'));

-- CREATE INDEX token_id_idx ON wallet_token_balance (token_id, time DESC);
-- CREATE INDEX wallet_id_idx ON wallet_token_balance (wallet_id, time DESC);

-- CREATE TABLE txn_record (
--     id SERIAL NOT NULL,
--     chain_id INT NOT NULL,
--     hash TEXT NOT NULL,
--     block_number INT NOT NULL,
--     from_address TEXT NOT NULL,
--     to_address TEXT NOT NULL,
--     token_address TEXT NOT NULL,
--     value DECIMAL(30,0) NOT NULL,
--     is_copied BOOLEAN NOT NULL,
--     time TIMESTAMPTZ PRIMARY KEY NOT NULL,
--     FOREIGN KEY (chain_id) REFERENCES chain(chain_id)
-- );

-- SELECT create_hypertable('txn_record', by_range('time'));

-- CREATE INDEX hash_idx ON public.txn_record (hash, time DESC);
-- CREATE INDEX block_number_idx ON txn_record (block_number, time DESC);
-- CREATE INDEX from_address_idx ON txn_record (from_address, time DESC);

-- CREATE TABLE pool_stats (
--     id SERIAL NOT NULL,
--     pool_dbank_id TEXT NOT NULL,
--     deposit_usd_value DECIMAL(20,5) NOT NULL,
--     deposit_user_count INT NOT NULL,
--     deposit_valable_user_count INT NOT NULL,
--     time TIMESTAMPTZ PRIMARY KEY NOT NULL
-- );

-- SELECT create_hypertable('pool_stats', by_range('time'));

-- CREATE INDEX pool_stats_idx ON pool_stats (pool_dbank_id, time DESC);

-- CREATE TABLE wallet_protocol_balance (
--     id SERIAL NOT NULL,
--     wallet_id INT NOT NULL,
--     protocol_dbank_id TEXT NOT NULL,
--     net_usd_value DECIMAL(20,5) NOT NULL,
--     asset_usd_value DECIMAL(20,5) NOT NULL,
--     debt_usd_value DECIMAL(20,5) NOT NULL,
--     time TIMESTAMPTZ PRIMARY KEY NOT NULL
-- );

-- SELECT create_hypertable('wallet_protocol_balance', by_range('time'));

-- CREATE INDEX wallet_protocol_id_idx ON wallet_protocol_balance (wallet_id, time DESC);

