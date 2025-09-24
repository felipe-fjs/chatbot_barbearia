"""adicionando RESERVED ao agendamentos.status

Revision ID: e50b3467fa7d
Revises: c1b4287a4cb1
Create Date: 2025-09-16 16:22:05.561296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e50b3467fa7d'
down_revision: Union[str, Sequence[str], None] = '85e698ddf72f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TABLE agendamentos "
        "MODIFY COLUMN status ENUM('FREE', 'REQUESTED', 'CONFIRMED', 'RESERVED') "
        "NOT NULL"
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
