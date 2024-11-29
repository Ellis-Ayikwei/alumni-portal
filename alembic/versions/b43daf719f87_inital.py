"""inital

Revision ID: b43daf719f87
Revises: c7da28c4ce54
Create Date: 2024-11-26 21:16:03.287458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b43daf719f87'
down_revision: Union[str, None] = 'c7da28c4ce54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('attachments_ibfk_1', 'attachments', type_='foreignkey')
    op.create_foreign_key(None, 'attachments', 'payments', ['payment_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'attachments', type_='foreignkey')
    op.create_foreign_key('attachments_ibfk_1', 'attachments', 'payments', ['payment_id'], ['id'])
    # ### end Alembic commands ###
