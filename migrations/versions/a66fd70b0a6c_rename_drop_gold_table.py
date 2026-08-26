"""rename drop_gold_table

Revision ID: a66fd70b0a6c
Revises: 4a62e9549894
Create Date: 2026-08-26 12:16:44.171467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a66fd70b0a6c'
down_revision: Union[str, Sequence[str], None] = '4a62e9549894'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table('gold_campaign_insights')
    pass


def downgrade() -> None:
    op.create_table('gold_campaign_insights',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('month', sa.String(), nullable=False),
        sa.Column('year', sa.String(), nullable=False),
        sa.Column('adset_name', sa.String(), nullable=True),
        sa.Column('impressions', sa.Numeric(), nullable=True),
        sa.Column('clicks', sa.Numeric(), nullable=True),
        sa.Column('spend', sa.Float(), nullable=True),
        sa.Column('cpm', sa.Float(), nullable=True),
        sa.Column('cpc', sa.Float(), nullable=True),
        sa.Column('cpp', sa.Float(), nullable=True),
        sa.Column('videos_view', sa.Numeric(), nullable=True),
        sa.Column('message_connection', sa.Numeric(), nullable=True),
        sa.Column('purchase', sa.Numeric(), nullable=True),
        sa.Column('cost_per_message', sa.Float(), nullable=True),
        sa.Column('cost_per_sale', sa.Float(), nullable=True),
        sa.Column('campaing_id', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('campaing_id', 'month', 'year', 'adset_name')
        )
    pass
