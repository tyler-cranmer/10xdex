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


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaleDB")

    op.create_table('wallet',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', sa.Text, nullable=False, unique=True),
        sa.Column('first_seen', sa.TIMESTAMP(timezone=True)),
        sa.Column('last_seen', sa.TIMESTAMP(timezone=True)),
        sa.Column('total_received', sa.Numeric, default=0),
        sa.Column('total_sent', sa.Numeric, default=0)
    )

    op.create_table('token',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', sa.Text, nullable=False, unique=True),
        sa.Column('name', sa.Text),
        sa.Column('symbol', sa.Text),
        sa.Column('decimal', sa.Integer)
    )

    op.create_table('ownership_history',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', sa.Text, nullable=False),
        sa.Column('token_address', sa.Text, nullable=False),
        sa.Column('tx_hash', sa.Text, nullable=False),
        sa.Column('block_number', sa.Integer, nullable=False),
        sa.Column('change', sa.Numeric(30, 0), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now())
    )
    op.execute("SELECT create_hypertable('ownership_history', 'timestamp')")

    op.create_table('wallet_token_balance',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('wallet_id', sa.Integer, nullable=False),
        sa.Column('token_id', sa.Integer, nullable=False),
        sa.Column('balance', sa.Numeric(30, 0), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id']),
        sa.ForeignKeyConstraint(['token_id'], ['token.id']),
        sa.UniqueConstraint('wallet_id', 'token_id', 'timestamp')
    )
    op.execute("SELECT create_hypertable('wallet_token_balance', 'timestamp')")

    op.create_table('transaction',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('tx_hash', sa.Text, nullable=False, unique=True),
        sa.Column('block_number', sa.Integer, nullable=False),
        sa.Column('from_address', sa.Text, nullable=False),
        sa.Column('to_address', sa.Text, nullable=False),
        sa.Column('token_address', sa.Text, nullable=False),
        sa.Column('value', sa.Numeric(30, 0), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False)
    )
    op.execute("SELECT create_hypertable('transaction', 'timestamp')")

    op.create_table('profit_loss',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('wallet_id', sa.Integer, nullable=False),
        sa.Column('token_id', sa.Integer, nullable=False),
        sa.Column('profit_loss', sa.Numeric, nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id']),
        sa.ForeignKeyConstraint(['token_id'], ['token.id']),
        sa.UniqueConstraint('wallet_id', 'token_id', 'timestamp')
    )
    op.execute("SELECT create_hypertable('profit_loss', 'timestamp')")

    op.create_table('price_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('token_address', sa.Text, nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('price', sa.Numeric, nullable=False),
        sa.UniqueConstraint('token_address', 'timestamp')
    )
    op.execute("SELECT create_hypertable('price_data', 'timestamp')")


def downgrade():
    op.drop_table('price_data')
    op.drop_table('profit_loss')
    op.drop_table('transaction')
    op.drop_table('wallet_token_balance')
    op.drop_table('ownership_history')
    op.drop_table('token')
    op.drop_table('wallet')
    op.execute("DROP EXTENSION IF EXISTS timescaleDB")