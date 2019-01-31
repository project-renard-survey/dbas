"""Remove user token from database

Revision ID: ed6cbcd62bee
Revises: 2f5bfca8d0e5
Create Date: 2019-01-09 18:50:34.084177

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ed6cbcd62bee'
down_revision = '2f5bfca8d0e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'token')
    op.drop_column('users', 'token_timestamp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('token_timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('token', sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###