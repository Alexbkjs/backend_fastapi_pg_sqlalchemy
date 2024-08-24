"""Initial migration

Revision ID: dfb2a01958f0
Revises: a48851e2df0e
Create Date: 2024-08-22 20:13:24.949795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfb2a01958f0'
down_revision: Union[str, None] = 'a48851e2df0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
