from datetime import datetime
from decimal import Decimal
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


class TokenBase(BaseModel):
    """ Base Token Model

    Base token to insert into database

    Attributes:
        address (str): The token address
        name (str): The token name
        symbol (str): The token symbol
        decimals (int): The token decimals

    """
    address: str
    name: str
    symbol: str
    decimal: int

class Token(TokenBase):
    """ Token Model from database

    Attributes:
        id (int): The token id
        address (str): The token address
        name (str): The token name
        symbol (str): The token symbol
        decimals (int): The token decimals
    """
    id: int


class OwnershipHistoryBase(BaseModel):
    """ Base Ownership History Model
    
    Attributes:
        address: The wallet address
        token_address: The token address
        tx_hash: The transaction hash
        block_number: The block number
        change: The change in ownership
        timestamp: The timestamp of the transaction
    """
    address: str
    token_address: str
    tx_hash: str
    block_number: int
    change: Decimal
    timestamp: datetime

class OwnershipHistory(OwnershipHistoryBase):
    """ Ownership History Model from database
    
    Attributes:
        id: The ownership history id
        address: The wallet address
        token_address: The token address
        tx_hash: The transaction hash
        block_number: The block number
        change: The change in ownership
        timestamp: The timestamp of the transaction
    """
    id: int


class WalletTokenBalanceBase(BaseModel):
    """ Base Wallet Token Balance Model

    Attributes:
        wallet_id: The wallet id
        token_id: The token id
        balance: The token balance
        timestamp: The timestamp of the balance
    """
    wallet_id: int
    token_id: int
    balance: Decimal
    timestamp: datetime


class WalletTokenBalance(WalletTokenBalanceBase):
    """
    Wallet Token Balance Model from database

    Attributes:
        id: The wallet token id
        wallet_id: The wallet id
        token_id: The token id
        balance: The token balance
        timestamp: The timestamp of the balance
    """
    id: int


class TransactionBase(BaseModel):
    """
    Transaction Base Model

    Attributes:
        tx_hash: The transaction hash
        block_number: The block number
        from_address: The sender address
        to_address: The receiver address
        token_address: The token address
        value: The token value
        timestamp: The timestamp of the transaction
    """
    tx_hash: str
    block_number: int
    from_address: str
    to_address: str
    token_address: str
    value: Decimal
    timestamp: datetime

class Transaction(TransactionBase):
    """ Transaction Model from database

    Attributes:
        id: The transaction id
        tx_hash: The transaction hash
        block_number: The block number
        from_address: The sender address
        to_address: The receiver address
        token_address: The token address
        value: The token value
        timestamp: The timestamp of the transaction
    """
    id: int

class ProfitLossBase(BaseModel):
    """ Base Profit Loss Model

    Attributes:
        wallet_address: The wallet address
        token_address: The token address
        profit_loss: The profit or loss
        timestamp: The timestamp of the profit or loss
    """
    wallet_address: str
    token_address: str
    profit_loss: Decimal
    timestamp: datetime

class ProfitLoss(ProfitLossBase):
    """ Profit Loss Model from database

    Attributes:
        id: The profit loss id
        wallet_address: The wallet address
        token_address: The token address
        profit_loss: The profit or loss
        timestamp: The timestamp of the profit or loss
    """
    id: int


class PriceDataBase(BaseModel):
    """ Base Price Data Model

    Attributes:
        token_address: The token address
        price: The token price
        timestamp: The timestamp of the price
    """
    token_address: str
    price: Decimal
    timestamp: datetime

class PriceData(PriceDataBase):
    """ Price Data Model from database

    Attributes:
        id: The price data id
        token_address: The token address
        price: The token price
        timestamp: The timestamp of the price
    """
    id: int
    