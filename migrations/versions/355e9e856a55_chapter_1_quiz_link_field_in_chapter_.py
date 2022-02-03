"""chapter 1 quiz link field in chapter table

Revision ID: 355e9e856a55
Revises: 8868fc0abe31
Create Date: 2022-02-03 07:51:31.575389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '355e9e856a55'
down_revision = '8868fc0abe31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chapter_1_quiz_link', sa.String(length=140), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.drop_column('chapter_1_quiz_link')

    # ### end Alembic commands ###
