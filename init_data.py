from db import TokenDB
from schema import CoinGeckoToken, TokenBase, ContractAddressJson
from config import Settings
import httpx
import json
from utils import get_key, split_and_replace, print_functions

s = Settings()


def get_coin_gecko_tokens():

    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    headers = {"accept": "application/json", "x-cg-pro-api-key": s.coin_gecko_api_key}

    response = httpx.get(url, headers=headers)
    tokens = [CoinGeckoToken(**token) for token in response.json()]
    base_tokens = [token for token in tokens if "base" in token.platforms]
    db_tokens = [
        TokenBase(address=token.platforms['base'], name=token.name, symbol=token.symbol, decimal=0)
        for token in base_tokens
    ]
    return db_tokens

def parse_contract_address():
    with open('contract_addresses.json') as f:
        data = json.load(f)


    contracts = []
    for address in data.values():

        folder, file = split_and_replace(get_key(address, data))
        contract = ContractAddressJson(folder=folder, file=file, address=address)
        contracts.append(contract.model_dump())

    with open('parsed_contract_addresses.json', 'w') as f:
        json.dump(contracts, f, indent=4)
    
    return contracts

def main():
    with open('parsed_contract_addresses.json') as f:
        data = json.load(f)

    keywords = ["Uniswap", "Uniswap_V3"]
    for contract in data:
        if any(keyword in contract['folder'] for keyword in keywords):
            with open(f"abis/{contract['folder']}/{contract['file']}.json") as f:
                abi = json.load(f)
                print(f"Protocol: {contract['folder']}, Contract: {contract['file']}")
                print_functions(abi)



if __name__ == "__main__":
    # main()
    tokens = get_coin_gecko_tokens()

    for token in tokens: 
        if token.name == 'doginme':
            print(token)





# Connect to web 3 provider

