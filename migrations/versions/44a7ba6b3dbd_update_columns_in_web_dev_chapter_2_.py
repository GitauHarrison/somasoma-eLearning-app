"""update columns in web dev chapter 2 quiz 2 table

Revision ID: 44a7ba6b3dbd
Revises: 29aa81426df9
Create Date: 2022-01-12 11:08:34.035061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44a7ba6b3dbd'
down_revision = '29aa81426df9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter_1_quiz_2_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('answer', sa.String(length=140), nullable=True))
        batch_op.drop_column('option_4')
        batch_op.drop_column('option_3')
        batch_op.drop_column('option_1')
        batch_op.drop_column('option_2')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter_1_quiz_2_options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('option_2', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('option_1', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('option_3', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('option_4', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('answer')

    # ### end Alembic commands ###
