"""Change tID column type to bigint

Revision ID: dae151c811f1
Revises: dfb2a01958f0
Create Date: 2024-08-25 12:05:29.380877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dae151c811f1'
down_revision: Union[str, None] = 'dfb2a01958f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Alter the tID column to bigint
    op.alter_column('users', 'tID',
                    type_=sa.BigInteger(),
                    existing_type=sa.Integer(),
                    existing_nullable=False)

def downgrade():
    # Revert the column type change if needed
    op.alter_column('users', 'tID',
                    type_=sa.Integer(),
                    existing_type=sa.BigInteger(),
                    existing_nullable=False)