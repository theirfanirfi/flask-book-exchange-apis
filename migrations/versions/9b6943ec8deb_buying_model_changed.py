"""buying model changed

Revision ID: 9b6943ec8deb
Revises: b2d7b2d8c183
Create Date: 2021-08-03 21:48:37.919128

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9b6943ec8deb'
down_revision = 'b2d7b2d8c183'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('buy_book', sa.Column('user_id', sa.String(length=200), nullable=False))
    op.drop_column('buy_book', 'buyer_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('buy_book', sa.Column('buyer_id', mysql.VARCHAR(length=200), nullable=False))
    op.drop_column('buy_book', 'user_id')
    # ### end Alembic commands ###
