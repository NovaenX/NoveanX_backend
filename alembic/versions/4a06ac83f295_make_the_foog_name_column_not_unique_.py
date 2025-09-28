"""make the foog_name column not unique, this allows the frontend to add multiple rows.

Revision ID: 4a06ac83f295
Revises: 
Create Date: 2025-09-28 15:27:42.993799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a06ac83f295'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Explicitly create indexes
    op.create_index("ix_food_logs_id", "food_logs", ["id"])
    op.create_index("ix_food_logs_food_name", "food_logs", ["food_name"])
