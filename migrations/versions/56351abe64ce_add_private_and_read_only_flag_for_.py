"""Add private and read-only flag for issues

Revision ID: 56351abe64ce
Revises: 42d481d084b2
Create Date: 2017-11-27 11:09:44.511103

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '56351abe64ce'
down_revision = '42d481d084b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('issues', sa.Column('is_private', sa.Boolean(), server_default='False', nullable=False))
    op.add_column('issues', sa.Column('is_read_only', sa.Boolean(), server_default='False', nullable=False))
    connection = op.get_bind()
    connection.execute("update issues set is_read_only = true where uid = 7")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('issues', 'is_read_only')
    op.drop_column('issues', 'is_private')
    # ### end Alembic commands ###
