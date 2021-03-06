"""comment column changed

Revision ID: 786e1194d6d1
Revises: c49e470dfda4
Create Date: 2021-04-04 13:22:55.607631

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '786e1194d6d1'
down_revision = 'c49e470dfda4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('comment_id', sa.String(length=200), nullable=False))
    op.drop_column('comments', 'c_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('c_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_column('comments', 'comment_id')
    # ### end Alembic commands ###
