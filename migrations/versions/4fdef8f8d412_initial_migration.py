"""initial migration

Revision ID: 4fdef8f8d412
Revises: 
Create Date: 2021-05-01 12:18:10.273591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fdef8f8d412'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('book_isbn', sa.String(length=200), nullable=False),
    sa.Column('book_title', sa.String(length=200), nullable=False),
    sa.Column('book_description', sa.Text(), nullable=True),
    sa.Column('book_author', sa.Text(), nullable=True),
    sa.Column('book_cover_image', sa.Text(), nullable=True),
    sa.Column('user_id', sa.String(length=200), nullable=False),
    sa.Column('book_added_from', sa.String(length=200), nullable=False),
    sa.Column('is_available_for_exchange', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('book_id')
    )
    op.create_table('categories',
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('cat_title', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('cat_id')
    )
    op.create_table('chat_messages',
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.String(length=200), nullable=False),
    sa.Column('message_text', sa.Text(), nullable=False),
    sa.Column('receiver_id', sa.String(length=200), nullable=False),
    sa.Column('is_message', sa.Integer(), nullable=True),
    sa.Column('is_exchange', sa.Integer(), nullable=True),
    sa.Column('exchange_id', sa.String(length=200), nullable=True),
    sa.Column('p_id', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('message_id')
    )
    op.create_table('chat_participants',
    sa.Column('p_id', sa.String(length=200), nullable=False),
    sa.Column('user_one_id', sa.String(length=200), nullable=False),
    sa.Column('user_two_id', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('p_id')
    )
    op.create_table('comments',
    sa.Column('comment_id', sa.String(length=200), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=200), nullable=False),
    sa.Column('comment_text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_table('exchange',
    sa.Column('exchange_id', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.String(length=200), nullable=False),
    sa.Column('to_exchange_with_user_id', sa.String(length=200), nullable=False),
    sa.Column('book_to_be_sent_id', sa.Integer(), nullable=False),
    sa.Column('book_to_be_received_id', sa.Integer(), nullable=False),
    sa.Column('is_exchange_confirmed', sa.Integer(), nullable=True),
    sa.Column('is_exchange_declined', sa.Integer(), nullable=True),
    sa.Column('exchange_message', sa.Text(), nullable=True),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('exchange_id')
    )
    op.create_table('followers',
    sa.Column('follow_id', sa.String(length=200), nullable=False),
    sa.Column('follower_user_id', sa.String(length=200), nullable=False),
    sa.Column('followed_user_id', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('follow_id')
    )
    op.create_table('likes',
    sa.Column('like_id', sa.String(length=200), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('like_id')
    )
    op.create_table('list',
    sa.Column('list_id', sa.Integer(), nullable=False),
    sa.Column('list_title', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('list_id')
    )
    op.create_table('notifications',
    sa.Column('notification_id', sa.String(length=200), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=200), nullable=False),
    sa.Column('to_be_notified_user_id', sa.String(length=200), nullable=False),
    sa.Column('exchange_id', sa.String(length=200), nullable=False),
    sa.Column('is_like', sa.Integer(), nullable=False),
    sa.Column('is_comment', sa.Integer(), nullable=False),
    sa.Column('is_follow', sa.Integer(), nullable=False),
    sa.Column('is_exchange', sa.Integer(), nullable=False),
    sa.Column('is_exchange_confirmed', sa.Integer(), nullable=False),
    sa.Column('is_exchange_declined', sa.Integer(), nullable=False),
    sa.Column('book_to_be_provided_id', sa.Integer(), nullable=False),
    sa.Column('book_requested_id', sa.Integer(), nullable=False),
    sa.Column('is_notification_read', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('notification_id')
    )
    op.create_table('post',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('post_title', sa.String(length=200), nullable=False),
    sa.Column('post_description', sa.Text(), nullable=True),
    sa.Column('post_image', sa.Text(), nullable=True),
    sa.Column('post_category', sa.Integer(), nullable=True),
    sa.Column('is_admin_post', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('stacks',
    sa.Column('stack_id', sa.String(length=200), nullable=False),
    sa.Column('list_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('stack_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.String(length=200), nullable=False),
    sa.Column('fullname', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('token', sa.String(length=200), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('is_admin', sa.Integer(), nullable=True),
    sa.Column('profile_image', sa.Text(), nullable=True),
    sa.Column('location_longitude', sa.String(length=50), nullable=True),
    sa.Column('location_latitude', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.String(length=50), nullable=True),
    sa.Column('updated_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('stacks')
    op.drop_table('post')
    op.drop_table('notifications')
    op.drop_table('list')
    op.drop_table('likes')
    op.drop_table('followers')
    op.drop_table('exchange')
    op.drop_table('comments')
    op.drop_table('chat_participants')
    op.drop_table('chat_messages')
    op.drop_table('categories')
    op.drop_table('book')
    # ### end Alembic commands ###
