"""remove review link field in Chapter table to improve UX for the teacher

Revision ID: 338d202f7dee
Revises: 2ae902861d50
Create Date: 2022-02-02 15:51:05.304941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '338d202f7dee'
down_revision = '2ae902861d50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.drop_column('chapter_review_link')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chapter_review_link', sa.VARCHAR(length=140), nullable=True))

    # ### end Alembic commands ###
