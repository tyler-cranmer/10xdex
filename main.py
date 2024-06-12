from utils import load_checkpoint, save_checkpoint, Web3Logic
from config import Settings

s = Settings()


def main():

    doginme = "0x6921b130d297cc43754afba22e5eac0fbf8db75b"
    # uniswap
    # LOAD CHECKPOINT
    CHECKPOINT_FILE = "checkpoint.json"
    checkpoint = load_checkpoint(CHECKPOINT_FILE)

    start_block = checkpoint["last_processed_block"]

    print(f"{start_block}")
    # WEB3 LOGIC
    web3_logic = Web3Logic(s.alchemy_rpc)
    # end_block = start_block + 1000
    end_block = web3_logic.w3.eth.block_number
    diff = end_block - start_block
    calls = diff // 1000
    print(end_block)
    print(diff)
    print(calls)
    print(calls * 2)

    
    # logs = web3_logic.fetch_transfer_logs(doginme, start_block, end_block)
    # logs = web3_logic.fetch_swap_logs(doginme, start_block, end_block)
    
    # process_swap_logs returns a generator object
    # logs_generator = web3_logic.process_logs(logs)

    # You can print out the information from the generator like this:
    # for log in logs_generator:
    #     print(log)

    # print(len(logs))


if __name__ == "__main__":
    main()
