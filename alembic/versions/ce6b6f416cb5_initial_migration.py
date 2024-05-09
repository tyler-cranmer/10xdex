"""Initial migration

Revision ID: ce6b6f416cb5
Revises: 
Create Date: 2024-05-08 10:09:14.916197

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "ce6b6f416cb5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None: 
    # Create 'chain' table
    op.create_table(
        "chain",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("chain_id", sa.Integer, unique=True, nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("native_token", sa.Text, nullable=False),
        sa.Column("wrapped_token_address", sa.Text, nullable=False),
        sa.Column("dbank_id", sa.Text, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    # Create 'token' table
    op.create_table(
        "token",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("chain_id", sa.Integer, nullable=False),
        sa.Column("address", sa.Text, nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("symbol", sa.Text, nullable=False),
        sa.Column("decimals", sa.Integer, nullable=False),
        sa.Column("usd_value", sa.DECIMAL(precision=20, scale=5), nullable=False),
        sa.Column(
            "usd_check",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["chain_id"], ["chain.chain_id"]),
        sa.UniqueConstraint("chain_id", "address", "name", "symbol"),
    )

    # Create 'wallet' table
    op.create_table(
        "wallet",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("chain_id", sa.Integer, nullable=False),
        sa.Column("address", sa.Text, nullable=False),
        sa.Column("private_key", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["chain_id"], ["chain.chain_id"]),
        sa.UniqueConstraint("chain_id", "address"),
    )

    # Create 'protocol' table
    op.create_table(
        "protocol",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("chain_id", sa.Integer, nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("tvl", sa.DECIMAL(precision=20, scale=5), nullable=False),
        sa.Column(
            "tvl_check",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("site_url", sa.Text, nullable=False),
        sa.Column("dbank_id", sa.Text, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["chain_id"], ["chain.chain_id"]),
    )

    # Create 'pool' table
    op.create_table(
        "pool",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("dbank_id", sa.Text, nullable=False),
        sa.Column("protocol_dbank_id", sa.TEXT, nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("controller", sa.Text, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["protocol_dbank_id"], ["protocol.id"]),
    )

    # Create 'pool_contract' table
    op.create_table(
        "pool_contract",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("pool_dbank_id", sa.Text, nullable=False),
        sa.Column("address", sa.Text, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["pool_dbank_id"], ["pool.dbank_id"]),
    )

    op.create_table(
        "wallet_token_balance",
        sa.Column("id", sa.Integer, autoincrement=True, nullable=False),
        sa.Column("wallet_id", sa.Integer, nullable=False),
        sa.Column("token_id", sa.Integer, nullable=False),
        sa.Column("balance", sa.DECIMAL(precision=30, scale=0), nullable=False),
        sa.Column(
            "time",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            primary_key=True,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["wallet_id"],
            ["wallet.id"],
        ),
        sa.ForeignKeyConstraint(
            ["token_id"],
            ["token.id"],
        ),
    )

    # Execute the hypertable creation using TimescaleDB's function
    op.execute("SELECT create_hypertable('wallet_token_balance', 'time');")

    # Create indexes
    op.create_index(
        "token_id_idx",
        "wallet_token_balance",
        ["token_id", "time"],
        unique=False,
        postgresql_using="btree",
        postgresql_ops={"time": "DESC"},
    )
    op.create_index(
        "wallet_id_idx",
        "wallet_token_balance",
        ["wallet_id", "time"],
        unique=False,
        postgresql_using="btree",
        postgresql_ops={"time": "DESC"},
    )

    # Create txn record table
    op.create_table(
        "txn_record",
        sa.Column("id", sa.Integer, autoincrement=True, nullable=False),
        sa.Column("chain_id", sa.Integer, nullable=False),
        sa.Column("hash", sa.Text, nullable=False),
        sa.Column("block_number", sa.Integer, nullable=False),
        sa.Column("from_address", sa.Text, nullable=False),
        sa.Column("to_address", sa.Text, nullable=False),
        sa.Column("token_address", sa.Text, nullable=False),
        sa.Column("value", sa.DECIMAL(precision=30, scale=0), nullable=False),
        sa.Column("is_copied", sa.Boolean, nullable=False),
        sa.Column(
            "time",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            primary_key=True,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["chain_id"], ["chain.chain_id"]),
    )

    # Convert table to a hypertable using TimescaleDB's function
    op.execute("SELECT create_hypertable('txn_record', 'time');")

    # Create indexes
    op.create_index(
        "hash_idx",
        "txn_record",
        ["hash", "time"],
        unique=False,
        postgresql_using="btree",
        postgresql_ops={"time": "DESC"},
    )
    op.create_index(
        "block_number_idx",
        "txn_record",
        ["block_number", "time"],
        unique=False,
        postgresql_using="btree",
        postgresql_ops={"time": "DESC"},
    )
    op.create_index(
        "from_address_idx",
        "txn_record",
        ["from_address", "time"],
        unique=False,
        postgresql_using="btree",
        postgresql_ops={"time": "DESC"},
    )

    op.create_table(
        "pool_stats",
        sa.Column("id", sa.Integer, autoincrement=True, nullable=False),
        sa.Column("pool_dbank_id", sa.Text, nullable=False),
        sa.Column(
            "deposited_usd_value", sa.DECIMAL(precision=20, scale=5), nullable=False
        ),
        sa.Column("deposited_user_count", sa.Integer, nullable=False),
        sa.Column("deposited_valable_user_count", sa.Integer, nullable=False),
        sa.Column(
            "time",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            primary_key=True,
            nullable=False,
        ),
    )

    # Convert table to a hypertable using TimescaleDB's function
    op.execute("SELECT create_hypertable('pool_stats', 'time');")

    # Create index
    op.create_index(
        "pool_stats_idx",
        "pool_stats",
        ["pool_dbank_id", "time"],
        unique=False,
        postgresql_using="btree",
        postgresql_ops={"time": "DESC"},
    )

    # Create 'wallet_protocol_balance' table
    op.create_table(
        "wallet_protocol_balance",
        sa.Column("id", sa.Integer, autoincrement=True, nullable=False),
        sa.Column("wallet_id", sa.Integer, nullable=False),
        sa.Column("protocol_dbank_id", sa.Text, nullable=False),
        sa.Column("net_usd_value", sa.DECIMAL(precision=20, scale=5), nullable=False),
        sa.Column("asset_usd_value", sa.DECIMAL(precision=20, scale=5), nullable=False),
        sa.Column("debt_usd_value", sa.DECIMAL(precision=20, scale=5), nullable=False),
        sa.Column(
            "time",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            primary_key=True,
            nullable=False,
        ),
    )

    # Convert table to a hypertable using TimescaleDB's function
    op.execute("SELECT create_hypertable('wallet_protocol_balance', 'time');")

    # Create index
    op.create_index(
        "wallet_protocol_id_idx",
        "wallet_protocol_balance",
        ["wallet_id", "time"],
        unique=False,
        postgresql_using="btree",
        postgresql_ops={"time": "DESC"},
    )


def downgrade() -> None:
    # Drop indices for 'wallet_protocol_balance' table
    op.drop_index("wallet_protocol_id_idx", table_name="wallet_protocol_balance")
    # Drop 'wallet_protocol_balance' table
    op.drop_table("wallet_protocol_balance")

    # Drop indices for 'pool_stats' table
    op.drop_index("pool_stats_idx", table_name="pool_stats")
    # Drop 'pool_stats' table
    op.drop_table("pool_stats")

    # Drop indices for 'txn_record' table
    op.drop_index("hash_idx", table_name="txn_record")
    op.drop_index("block_number_idx", table_name="txn_record")
    op.drop_index("from_address_idx", table_name="txn_record")
    # Drop 'txn_record' table
    op.drop_table("txn_record")

    # Drop indices for 'wallet_token_balance' table
    op.drop_index("token_id_idx", table_name="wallet_token_balance")
    op.drop_index("wallet_id_idx", table_name="wallet_token_balance")
    # Drop 'wallet_token_balance' table
    op.drop_table("wallet_token_balance")

    # Drop 'pool_contract' table
    op.drop_table("pool_contract")

    # Drop 'pool' table
    op.drop_table("pool")

    # Drop 'protocol' table
    op.drop_table("protocol")

    # Drop 'wallet' table
    op.drop_table("wallet")

    # Drop 'token' table
    op.drop_table("token")

    # Drop 'chain' table
    op.drop_table("chain")
