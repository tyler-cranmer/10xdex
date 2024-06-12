from datetime import datetime
import json

# Function to get the key from a value in a dictionary. Used to get the name of the contract from the address.
def get_key(val, data):
    for key, value in data.items():
        if val in value:
            return key
    return "key doesn't exist"



# Function to split the input string by a delimiter and replace spaces with underscores
def split_and_replace(s, delimiter=':'):
    parts = s.split(delimiter)
    if len(parts) != 2:
        raise ValueError("Input string should contain exactly one delimiter")
    folder = parts[0].strip().replace(' ', '_')
    file = parts[1].strip().replace(' ', '_')
    return folder, file






def load_checkpoint(checkpoint_file: str):
    try:
        with open(checkpoint_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'last_processed_block': 0}

def save_checkpoint(checkpoint_file:str , last_processed_block: int):
    with open(checkpoint_file, 'w') as f:
        json.dump({'last_processed_block': last_processed_block}, f)




def convert_block_timestamp(block_timestamp):
    return datetime.fromtimestamp(block_timestamp, tz=datetime.timezone.utc)
