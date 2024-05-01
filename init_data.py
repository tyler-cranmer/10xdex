"""
This script fetches the initial data to populate the database.

It fetches the chains, tokens, protocols, and pools from the Debank API and inserts them into the database.


"""

import requests
from db import ChainDB, TokenDB
from config import Settings
from schema import ChainBase, TokenBase
from datetime import datetime, timezone

s = Settings()


def fetch_dbbank(url: str):
    try:
        headers = {"accept": "application/json", "AccessKey": s.debank_api_key}
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise


def insert_chains():

    chains = fetch_dbbank("https://pro-openapi.debank.com/v1/chain/list")
    chain_db = ChainDB()
    chain_names = []

    for _, chain in enumerate(chains):
        wt = chain["wrapped_token_id"]
        if wt is None:
            wt = "none"
        x = chain_db.insert(
            ChainBase(
                chain_id=chain["community_id"],
                name=chain["name"],
                native_token=chain["native_token_id"],
                wrapped_token_address=wt,
                dbank_id=chain["id"],
            )
        )
        chain_names.append(x.name)
    print(f"Inserted chains: {chain_names}")


def insert_chain_wrapped_tokens():
    chain_db = ChainDB()
    token_db = TokenDB()
    chains = chain_db.get_all_chains()
    token_list = []
    for chain in chains:
        token = chain.wrapped_token_address
        db_id = chain.dbank_id
        if token == "" or token is None:
            continue
        url = f"https://pro-openapi.debank.com/v1/token?chain_id={db_id}&id={token}"
        token_info = fetch_dbbank(url)

        token = token_db.insert(
            TokenBase(
                name=token_info["name"],
                symbol=token_info["symbol"],
                address=token_info["id"],
                decimals=token_info["decimals"],
                usd_value=token_info["price"],
                usd_check=datetime.now(timezone.utc),
                chain_id=chain.chain_id,
            )
        )

        token_list.append(token.name)
    print(f"Inserted tokens: {token_list}")


def fetch_insert_protocols():
    pass


def fetch_insert_pools():

    pass


def main():
    insert_chains()
    insert_chain_wrapped_tokens()


if __name__ == "__main__":
    main()
