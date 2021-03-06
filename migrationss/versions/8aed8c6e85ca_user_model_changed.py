"""user model changed

Revision ID: 8aed8c6e85ca
Revises: 786e1194d6d1
Create Date: 2021-04-05 11:21:42.267821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8aed8c6e85ca'
down_revision = '786e1194d6d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('location_latitude', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('location_longitue', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'location_longitue')
    op.drop_column('users', 'location_latitude')
    # ### end Alembic commands ###
