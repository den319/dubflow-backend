"""add name field and make original_file_name nullable in projects

Revision ID: 5f053dcacefd
Revises: 951088881375
Create Date: 2026-06-22 17:08:25.840173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f053dcacefd'
down_revision: Union[str, Sequence[str], None] = '951088881375'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add name column as nullable first (existing rows have no name)
    op.add_column('projects', sa.Column('name', sa.String(), nullable=True))

    # 2. Backfill existing rows with their original_file_name as the project name
    op.execute("UPDATE projects SET name = COALESCE(original_file_name, 'Untitled Project') WHERE name IS NULL")

    # 3. Now set name to NOT NULL
    op.alter_column('projects', 'name', nullable=False)

    # 4. Make original_file_name nullable
    op.alter_column('projects', 'original_file_name',
               existing_type=sa.VARCHAR(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('projects', 'original_file_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('projects', 'name')