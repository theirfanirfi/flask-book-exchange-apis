"""selling functionality is being added

Revision ID: ec17418e0d72
Revises: 304b783476f3
Create Date: 2021-08-02 13:47:31.543247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec17418e0d72'
down_revision = '304b783476f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('is_for_sale', sa.Integer(), nullable=True))
    op.add_column('book', sa.Column('selling_price', sa.Float(), nullable=True))
    op.add_column('exchange', sa.Column('is_for_sale', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exchange', 'is_for_sale')
    op.drop_column('book', 'selling_price')
    op.drop_column('book', 'is_for_sale')
    # ### end Alembic commands ###
