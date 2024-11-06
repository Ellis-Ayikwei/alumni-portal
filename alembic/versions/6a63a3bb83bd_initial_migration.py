"""Initial migration

Revision ID: 6a63a3bb83bd
Revises: 42d861d17526
Create Date: 2024-11-06 16:37:53.932435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a63a3bb83bd'
down_revision: Union[str, None] = '42d861d17526'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('beneficiaries', sa.Column('group_member_id', sa.String(length=60), nullable=True))
    op.create_foreign_key(None, 'beneficiaries', 'group_members', ['group_member_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'beneficiaries', type_='foreignkey')
    op.drop_column('beneficiaries', 'group_member_id')
    # ### end Alembic commands ###