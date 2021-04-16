"""notification and exchange models changed

Revision ID: 32fb2b9eaa57
Revises: e186720b79b6
Create Date: 2021-04-17 02:08:29.562852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32fb2b9eaa57'
down_revision = 'e186720b79b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exchange', sa.Column('is_exchange_declined', sa.Integer(), nullable=True))
    op.add_column('notifications', sa.Column('is_exchange_confirmed', sa.Integer(), nullable=False))
    op.add_column('notifications', sa.Column('is_exchange_declined', sa.Integer(), nullable=False))
    op.add_column('notifications', sa.Column('is_notification_read', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notifications', 'is_notification_read')
    op.drop_column('notifications', 'is_exchange_declined')
    op.drop_column('notifications', 'is_exchange_confirmed')
    op.drop_column('exchange', 'is_exchange_declined')
    # ### end Alembic commands ###
