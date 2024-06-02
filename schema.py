from datetime import datetime
from pydantic import BaseModel

class WalletBase(BaseModel):
    """ Base Wallet Model

    Base wallet to insert into database

    Attributes:
        address (str): The wallet address
        first_seen (datetime): The first time the wallet was seen
        last_seen (datetime): The last time the wallet was seen
        total_received (int): The total amount received by the wallet
        total_sent (int): The total amount sent by the wallet

    """
    address: str
    first_seen: datetime
    last_seen: datetime
    total_received: int
    total_sent: int

class Wallet(WalletBase):
    """ Wallet Model from database

    Attributes:
        id (int): The wallet id
        address (str): The wallet address
        first_seen (datetime): The first time the wallet was seen
        last_seen (datetime): The last time the wallet was seen
        total_received (int): The total amount received by the wallet
        total_sent (int): The total amount sent by the wallet
    """
    id: int