from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
from decimal import Decimal


class ChainBase(BaseModel):
    """
    Base data class for Chain.

    Attributes:
        chain_id: The id of the chain.
        name: The name of the chain.
        native_token: The native token of the chain.
        wrapped_token_address: The address of the wrapped token on the chain.
        dbank_id: The id of the dbank associated with the chain.
    """
    chain_id: int
    dbank_id: str
    name: str
    native_token: str
    wrapped_token_address: str
    
    


class Chain(ChainBase):
    """
    Data class for Chain, extends ChainBase.

    Attributes:
        id: A unique identifier for the chain.
        
    Inherited:
        chain_id: The id of the chain.
        name: The name of the chain.
        native_token: The native token of the chain.
        wrapped_token_address: The address of the wrapped token on the chain.
        dbank_id: The id of the dbank associated with the chain.
        created_at: The datetime when the chain was created.
    """
    id: int
    created_at: datetime


class TokenBase(BaseModel):
    """
    Base data class for Token.

    Attributes:
        name: The name of the token.
        symbol: The symbol of the token.
        address: The address of the token.
        decimals: The number of decimals the token uses.
        chain_id: The id of the chain the token belongs to.
        usd_value: The USD value of the token. Defaults to Decimal(0) if not provided.
        usd_check: The datetime when the USD value was checked.
    """
    name: str
    symbol: str
    address: str
    decimals: int
    chain_id: int
    usd_value: Optional[Decimal] = None
    usd_check: datetime

    @field_validator("usd_value")
    def validate_usd_value(cls, v):
        """
        Validator for the 'usd_value' field. If the value is None, it defaults to Decimal(0).

        Args:
            v: The value to validate.

        Returns:
            The validated value.
        """
        if v is None:
            return Decimal(0)
        return v


class Token(TokenBase):
    """
    Data class for Token, extends TokenBase.

    Attributes:
        id: A unique identifier for the token.
        created_at: The datetime when the token was created.
    Inherited:
        name: The name of the token.
        symbol: The symbol of the token.
        address: The address of the token.
        decimals: The number of decimals the token uses.
        chain_id: The id of the chain the token belongs to.
        usd_value: The USD value of the token. Defaults to Decimal(0) if not provided.
        usd_check: The datetime when the USD value was checked.
    """
    id: int
    created_at: datetime


class ProtocolBase(BaseModel):
    """
    Base data class for Protocol.

    Attributes:
        chain_id: The id of the chain the protocol belongs to.
        name: The name of the protocol.
        tvl: The total value locked in the protocol. Defaults to Decimal(0) if not provided.
        tvl_check: The datetime when the total value locked was checked.
        site_url: The URL of the protocol's website. Defaults to "none" if not provided.
        dbank_id: The id of the dbank associated with the protocol.
    """
    chain_id: int
    name: str
    tvl: Optional[Decimal] = None
    tvl_check: datetime
    site_url: Optional[str] = None
    dbank_id: str

    @field_validator("site_url")
    def validate_site_url(cls, v):
        """
        Validator for the 'site_url' field. If the value is None, it defaults to "none".

        Args:
            v: The value to validate.

        Returns:
            The validated value.
        """
        if v is None:
            return "none"
        return v

    @field_validator("tvl")
    def validate_tvl(cls, v):
        """
        Validator for the 'tvl' field. If the value is None, it defaults to Decimal(0).

        Args:
            v: The value to validate.

        Returns:
            The validated value.
        """
        if v is None:
            return Decimal(0)
        return v

class Protocol(ProtocolBase):
    """
    Data class for Protocol, extends ProtocolBase.

    Attributes:
        id: A unique identifier for the protocol.
    Inherited:
        chain_id: The id of the chain the protocol belongs to.
        name: The name of the protocol.
        tvl: The total value locked in the protocol. Defaults to Decimal(0) if not provided.
        tvl_check: The datetime when the total value locked was checked.
        site_url: The URL of the protocol's website. Defaults to "none" if not provided.
        dbank_id: The id of the dbank associated with the protocol.
    """
    id: int


class PoolBase(BaseModel):
    """
    Base data class for Pool.

    Attributes:
        dbank_id: The id of the pool.
        protocol_dbank_id: The id of the protocol the pool belongs to.
        controller: The address of the controller of the pool.
        name: The name of the pool.
    """
    dbank_id: str
    protocol_dbank_id: str
    controller: str
    name: str


class Pool(PoolBase):
    """
    Data class for Pool, extends PoolBase.

    Attributes:
        id: A unique identifier for the pool.
        created_at: The datetime when the pool was created.
    Inherited:
        dbank_id: The id of the pool.
        protocol_dbank_id: The id of the protocol the pool belongs to.
        controller: The address of the controller of the pool.
        name: The name of the pool.
    """
    id: int
    created_at: datetime


class PoolContractBase(BaseModel):
    """
    Base data class for PoolContract.

    Attributes:
        pool_dbank_id: The id of the pool the contract belongs to.
        address: The address of the contract.
    """
    pool_dbank_id: str
    address: str


class PoolContract(PoolContractBase):
    """
    Data class for PoolContract, extends PoolContractBase.

    Attributes:
        id: A unique identifier for the pool contract.
        created_at: The datetime when the pool contract was created.
    Inherited:
        pool_dbank_id: The id of the pool the contract belongs to.
        address: The address of the contract.
    """
    id: int
    created_at: datetime


class PoolWithContracts(BaseModel):
    """
    Data class for PoolWithContracts.

    Attributes:
        pool: A Pool object.
        contracts: A list of PoolContract objects associated with the pool.
    """
    pool: Pool
    contracts: list[PoolContract]


class PoolStatsBase(BaseModel):
    """
    Base data class for PoolStats.

    Attributes:
        pool_dbank_id: The id of the pool the stats belong to.
        deposited_usd_value: The deposited USD value in the pool. Defaults to 0 if not provided.
        deposit_user_count: The number of users who deposited in the pool. Defaults to 0 if not provided.
        deposit_valuable_user_count: The number of valuable users who deposited in the pool. Defaults to 0 if not provided.
    """
    pool_dbank_id: str
    deposited_usd_value: Optional[Decimal] = None
    deposit_user_count: Optional[int] = None
    deposit_valuable_user_count: Optional[int] = None

    @field_validator("deposited_usd_value")
    def validate_deposited_usd_value(cls, v):
        """
        Validator for the 'deposited_usd_value' field. If the value is None, it defaults to Decimal(0).

        Args:
            v: The value to validate.

        Returns:
            The validated value.
        """
        if v is None:
            return Decimal(0)
        return v
    
    @field_validator("deposit_user_count", "deposit_valuable_user_count")
    def validate_deposit_user_count(cls, v):
        """
        Validator for the 'deposit_user_count' and 'deposit_valuable_user_count' fields. If the value is None, it defaults to 0.

        Args:
            v: The value to validate.

        Returns:
            The validated value.
        """
        if v is None:
            return 0
        return v

class PoolStats(PoolStatsBase):
    """
    Data class for PoolStats.

    Attributes:
        id: A unique identifier for the pool stats.
        time: The datetime when the pool stats were recorded.
    Inherited:
        pool_dbank_id: The id of the pool the stats belong to.
        deposited_usd_value: The deposited USD value in the pool. Defaults to 0 if not provided.
        deposit_user_count: The number of users who deposited in the pool. Defaults to 0 if not provided.
        deposit_valuable_user_count: The number of valuable users who deposited in the pool. Defaults to 0 if not provided.
    """
    id: int
    time: datetime


class WalletBase(BaseModel):
    """
    Base data class for Wallet.

    Attributes:
        address: The address of the wallet.
        chain_id: The id of the blockchain chain the wallet belongs to.
    """
    address: str
    chain_id: int


class Wallet(WalletBase):
    """
    Data class for Wallet, extends WalletBase.

    Attributes:
        id: A unique identifier for the wallet.
        created_at: The datetime when the wallet was created.
    Inherited:
        address: The address of the wallet.
        chain_id: The id of the blockchain chain the wallet belongs to.
    """
    id: int
    created_at: datetime


class WalletTokenBase(BaseModel):
    """
    Base data class for WalletToken.

    Attributes:
        wallet_id: The id of the wallet the token belongs to.
        token_id: The id of the token.
        balance: The balance of the token in the wallet.
    """
    wallet_id: int
    token_id: int
    balance: Decimal


class WalletToken(WalletTokenBase):
    """
    Data class for WalletToken, extends WalletTokenBase.

    Attributes:
        id: A unique identifier for the wallet token.
        time: The datetime when the wallet token balance was recorded.
    Inherited:
        wallet_id: The id of the wallet the token belongs to.
        token_id: The id of the token.
        balance: The balance of the token in the wallet.
    """
    id: int
    time: datetime


class TransactionBase(BaseModel):
    """
    Base data class for Transaction.

    Attributes:
        hash: The hash of the transaction.
        chain_id: The id of the chain the transaction belongs to.
        block_number: The number of the block the transaction is in.
        from_address: The address the transaction is from.
        to_address: The address the transaction is to.
        token_address: The address of the token being transacted.
        value: The value of the transaction.
    """
    hash: str
    chain_id: int
    block_number: int
    from_address: str
    to_address: str
    token_address: str
    value: Decimal


class Transaction(TransactionBase):
    """
    Data class for Transaction, extends TransactionBase.

    Attributes:
        id: A unique identifier for the transaction.
        created_at: The datetime when the transaction was created.]
    Inherited:
        hash: The hash of the transaction.
        chain_id: The id of the chain the transaction belongs to.
        block_number: The number of the block the transaction is in.
        from_address: The address the transaction is from.
        to_address: The address the transaction is to.
        token_address: The address of the token being transacted.
        value: The value of the transaction.
    """
    id: int
    created_at: datetime


class WalletProtocolBalanceBase(BaseModel):
    """
    Base data class for WalletProtocolBalance.

    Attributes:
        wallet_id: The id of the wallet.
        protocol_dbank_id: The id of the dbank protocol the balance belongs to.
        net_usd_value: The net USD value of the balance.
        asset_usd_value: The USD value of the assets in the balance.
        debt_usd_value: The USD value of the debt in the balance.
    """
    wallet_id: int
    protocol_dbank_id: str
    net_usd_value: Decimal
    asset_usd_value: Decimal
    debt_usd_value: Decimal


class WalletProtocolBalance(WalletProtocolBalanceBase):
    """
    Data class for WalletProtocolBalance, extends WalletProtocolBalanceBase.

    Attributes:
        id: A unique identifier for the wallet protocol balance.
        time: The datetime when the balance was recorded.
    Inherited:
        wallet_id: The id of the wallet.
        protocol_dbank_id: The id of the dbank protocol the balance belongs to.
        net_usd_value: The net USD value of the balance.
        asset_usd_value: The USD value of the assets in the balance.
        debt_usd_value: The USD value of the debt in the balance.
    """
    id: int
    time: datetime