"""Initial migration

Revision ID: b18ebc7af645
Revises: 14350a1317c4
Create Date: 2024-11-10 04:42:58.681166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b18ebc7af645'
down_revision: Union[str, None] = '14350a1317c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contracts', 'signed_date',
               existing_type=mysql.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contracts', 'signed_date',
               existing_type=sa.Date(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    # ### end Alembic commands ###
