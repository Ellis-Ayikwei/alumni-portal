"""Initial migration

Revision ID: bb70f33e8969
Revises: 9c85154e4dd0
Create Date: 2024-11-06 15:47:57.575061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'bb70f33e8969'
down_revision: Union[str, None] = '9c85154e4dd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('beneficiaries_ibfk_2', 'beneficiaries', type_='foreignkey')
    op.drop_column('beneficiaries', 'benefactor_group_memeber_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('beneficiaries', sa.Column('benefactor_group_memeber_id', mysql.VARCHAR(length=60), nullable=True))
    op.create_foreign_key('beneficiaries_ibfk_2', 'beneficiaries', 'group_members', ['benefactor_group_memeber_id'], ['id'])
    # ### end Alembic commands ###
