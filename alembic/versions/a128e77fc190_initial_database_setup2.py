"""Initial database setup2

Revision ID: a128e77fc190
Revises: 134d0495a01a
Create Date: 2024-08-27 19:38:17.723965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a128e77fc190'
down_revision: Union[str, None] = '134d0495a01a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
