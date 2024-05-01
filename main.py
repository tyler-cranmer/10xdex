import requests
from db import ChainDB, get_db
from config import Settings
from schema import ChainBase

s = Settings()


def fetch_insert_chains():
    with get_db() as db:
        chain_db = ChainDB(db)
        url = "https://pro-openapi.debank.com/v1/chain/list"
        headers = {"accept": "application/json", "AccessKey": s.debank_api_key}
        response = requests.get(url, headers=headers)
        chains = response.json()
        chain_names = []
        for _, chain in enumerate(chains):
            x = chain_db.insert(
                ChainBase(
                    chain_id=chain["community_id"],
                    name=chain["name"],
                    native_token=chain["native_token_id"],
                    wrapped_token_address=chain["wrapped_token_id"],
                )
            )
            chain_names.append(x.name)
        print(f"Inserted chains: {chain_names}")

def fetch_insert_tokens():
        url = "https://pro-openapi.debank.com/v1/chain/list"
        headers = {"accept": "application/json", "AccessKey": s.debank_api_key}
        response = requests.get(url, headers=headers)
        chains = response.json()
    
    


def main():
    fetch_insert_chains()


if __name__ == "__main__":
    main()
