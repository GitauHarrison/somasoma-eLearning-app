"""answer column in webdebchapter1_quiz4 table

Revision ID: 7d5a5b61ce40
Revises: d72ee76e6afa
Create Date: 2022-01-17 11:47:00.768584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d5a5b61ce40'
down_revision = 'd72ee76e6afa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter_1_quiz_4_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('answer', sa.String(length=140), nullable=True))
        batch_op.drop_column('option_1')
        batch_op.drop_column('option_2')
        batch_op.drop_column('option_4')
        batch_op.drop_column('option_3')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter_1_quiz_4_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('option_3', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('option_4', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('option_2', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('option_1', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('answer')

    # ### end Alembic commands ###
