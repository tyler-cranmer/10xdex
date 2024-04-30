CREATE TABLE chain (
    id INT PRIMARY KEY NOT NULL,
    chain_id INT NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    native_token VARCHAR(255) NOT NULL,
    wrapped_token_address VARCHAR(255) NOT NULL, 
    created_at TIMESTAMPZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE token (
    id INT PRIMARY KEY NOT NULL,
    chain_id INT NOT NULL,
    address VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    symbol VARCHAR(255) NOT NULL,
    decimals INT NOT NULL,
    usd_value DECIMAL(65, 18) NOT NULL,
    usd_check TIMESTAMPZ DEFAULT CURRENT_TIMESTAMP
    FOREIGN KEY (chain_id) REFERENCES chain(chain_id)
);


CREATE TABLE wallet (
    id INT PRIMARY KEY NOT NULL,
    chain_id INT NOT NULL,
    address VARCHAR(255) NOT NULL,
    created_at TIMESTAMPZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chain_id) REFERENCES chain(chain_id)
);








-- HYPER TABLES --

CREATE TABLE wallet_token_balance (
    id INT PRIMARY KEY NOT NULL,
    wallet_id INT NOT NULL,
    token_id INT NOT NULL,
    balance DECIMAL(65, 18) NOT NULL,
    time TIMESTAMPZ NOT NULL,
    FOREIGN KEY (wallet_id) REFERENCES wallet(id),
    FOREIGN KEY (token_id) REFERENCES token(id)
);

SELECT create_hypertable('wallet_token_balance', 'time');

CREATE INDEX token_id_idx ON wallet_token_balance (token_id, time DESC);
CREATE INDEX wallet_id_idx ON wallet_token_balance (wallet_id, time DESC);


CREATE TABLE txn_record (
    id INT PRIMARY KEY NOT NULL,
    chain_id INT NOT NULL,
    hash VARCHAR(255) NOT NULL,
    block_number INT NOT NULL,
    from_address VARCHAR(255) NOT NULL,
    to_address VARCHAR(255) NOT NULL,
    token_address VARCHAR(255) NOT NULL,
    amount DECIMAL(65, 18) NOT NULL,
    time TIMESTAMPZ NOT NULL,
    FOREIGN KEY (chain_id) REFERENCES chain(chain_id)
)

SELECT create_hypertable('txn_record', 'time');

CREATE INDEX hash_idx ON txn_record (hash, time DESC);