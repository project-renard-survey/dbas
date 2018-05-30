"""Move statements issue into new table

Revision ID: cfd456c47b69
Revises: f0bf03bf6326
Create Date: 2018-05-22 12:12:39.771294

"""
import sqlalchemy as sa
import transaction
from alembic import op
from sqlalchemy.sql import text

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, StatementToIssue
revision = 'cfd456c47b69'
down_revision = 'f0bf03bf6326'
branch_labels = None
depends_on = None


def upgrade():
    DBDiscussionSession.remove()
    DBDiscussionSession.configure(bind=op.get_bind())
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statement_to_issue',
                    sa.Column('uid', sa.Integer(), nullable=False),
                    sa.Column('statement_uid', sa.Integer(), nullable=False),
                    sa.Column('issue_uid', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['statement_uid'], ['statements.uid'], ),
                    sa.ForeignKeyConstraint(['issue_uid'], ['issues.uid'], ),
                    sa.PrimaryKeyConstraint('uid')
                    )

    connection = op.get_bind()
    for db_statement in DBDiscussionSession.query(Statement).all():
        issue_uid = connection.execute(text("""
            SELECT issue_uid
              FROM statements
             WHERE uid = :statement_uid
            """), {'statement_uid': db_statement.uid})
        DBDiscussionSession.add(StatementToIssue(statement=db_statement.uid, issue=issue_uid.first()[0]))

        DBDiscussionSession.flush()
    transaction.commit()
    op.drop_column('statements', 'issue_uid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('statements', sa.Column('issue_uid', sa.Integer(), server_default='1', nullable=False))
    for db_statement in DBDiscussionSession.query(Statement).all():
        db_statement2issue = DBDiscussionSession.query(StatementToIssue).filter_by(
            statement_uid=db_statement.uid).first()
        db_statement.issue_uid = db_statement2issue.issue_uid
        DBDiscussionSession.flush()
    transaction.commit()
    op.drop_table('statement_to_issue')
    # ### end Alembic commands ###