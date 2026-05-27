"""rename amount to amount_cents on expense, income, budget

Revision ID: 295c13898dd3
Revises: b88fce4ab045
Create Date: 2026-05-26 23:14:10.243367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '295c13898dd3'
down_revision: Union[str, Sequence[str], None] = 'b88fce4ab045'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('expense', 'amount', new_column_name='amount_cents')
    op.alter_column('income', 'amount', new_column_name='amount_cents')
    op.alter_column('budget', 'amount', new_column_name='amount_cents')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('budget', 'amount_cents', new_column_name='amount')
    op.alter_column('income', 'amount_cents', new_column_name='amount')
    op.alter_column('expense', 'amount_cents', new_column_name='amount')
