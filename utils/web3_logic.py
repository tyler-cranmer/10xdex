import time
from web3 import Web3


class Web3Logic:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

        if not self.w3.is_connected():
            raise ValueError("Web3 connection failed")

    def fetch_transfer_logs(
        self,
        token_address: str,
        start_block: int,
        end_block: int,
        retries=3,
    ):
        transfer_event_signature = self.w3.keccak(
            text="Transfer(address,address,uint256)"
        ).hex()
        logs = []

        attempt = 0
        while attempt < retries:
            try:
                filter_params = {
                    "fromBlock": start_block,
                    "toBlock": end_block,
                    "address": self.w3.to_checksum_address(token_address),
                    "topics": [transfer_event_signature],
                }
                logs.extend(self.w3.eth.get_logs(filter_params))
                return logs
            except Exception as e:
                print(f"Error fetching logs: {e}, retrying... ({attempt+1}/{retries})")
                time.sleep(2**attempt)
                attempt += 1
                continue

    def fetch_swap_logs(self, pair_address, start_block, end_block, batch_size=1000):
 
        swap_event_signature = self.w3.keccak(
            text="Swap(address,uint256,uint256,uint256,uint256,address)"
        ).hex()
 
        logs = []
        for block in range(start_block, end_block, batch_size):
            end = min(block + batch_size - 1, end_block)
            filter_params = {
                'fromBlock': block,
                'toBlock': end,
                'address': pair_address,
                'topics': [swap_event_signature]
            }
            logs.extend(self.w3.eth.get_logs(filter_params))
        
        return logs


    def process_swap_logs(self, logs):
        for log in logs:
            tx_hash = log["transactionHash"].hex()
            block_number = log["blockNumber"]
            from_address = self.w3.to_checksum_address(log["topics"][1][-20:])
            to_address = self.w3.to_checksum_address(log["data"][-20:])
            amount0_in = self.w3.to_int(hexstr=log["topics"][2])
            amount1_in = self.w3.to_int(hexstr=log["topics"][3])
            amount0_out = self.w3.to_int(hexstr=log["data"][:66])
            amount1_out = self.w3.to_int(hexstr=log["data"][66:])
            timestamp = self.get_block_timestamp(block_number)
            yield tx_hash, block_number, from_address, to_address, amount0_in, amount1_in, amount0_out, amount1_out, timestamp

    def process_logs(self, logs):
        for log in logs:
            from_address = "0x" + log["topics"][1].hex()[26:]
            to_address = "0x" + log["topics"][2].hex()[26:]
            value = int(log["data"].hex(), 16)
            tx_hash = log["transactionHash"].hex()
            block_number = log["blockNumber"]
            timestamp = self.get_block_timestamp(block_number)
            yield tx_hash, block_number, from_address, to_address, value, timestamp

    def get_block_timestamp(self, block_number: int):
        block = self.w3.eth.get_block(block_number)
        return block.timestamp
