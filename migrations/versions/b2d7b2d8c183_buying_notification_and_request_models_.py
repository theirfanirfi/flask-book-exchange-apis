"""buying notification and request models added

Revision ID: b2d7b2d8c183
Revises: ec17418e0d72
Create Date: 2021-08-03 21:32:16.305540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2d7b2d8c183'
down_revision = 'ec17418e0d72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buy_book',
    sa.Column('buy_id', sa.String(length=200), nullable=False),
    sa.Column('book_holder_id', sa.String(length=200), nullable=False),
    sa.Column('buyer_id', sa.String(length=200), nullable=False),
    sa.Column('book_id', sa.String(length=200), nullable=False),
    sa.Column('is_accepted', sa.Integer(), nullable=True),
    sa.Column('is_rejected', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('buy_id')
    )
    op.add_column('notifications', sa.Column('buy_id', sa.Integer(), nullable=False))
    op.add_column('notifications', sa.Column('is_for_sale', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notifications', 'is_for_sale')
    op.drop_column('notifications', 'buy_id')
    op.drop_table('buy_book')
    # ### end Alembic commands ###
