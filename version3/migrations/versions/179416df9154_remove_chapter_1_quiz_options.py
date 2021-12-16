"""remove chapter 1 quiz options

Revision ID: 179416df9154
Revises: ce38a67e37a8
Create Date: 2021-12-16 09:57:24.317678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '179416df9154'
down_revision = 'ce38a67e37a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter1_quiz', schema=None) as batch_op:
        batch_op.drop_column('quiz_1')
        batch_op.drop_column('quiz_4')
        batch_op.drop_column('quiz_3')
        batch_op.drop_column('quiz_2')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter1_quiz', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quiz_2', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('quiz_3', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('quiz_4', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('quiz_1', sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###
