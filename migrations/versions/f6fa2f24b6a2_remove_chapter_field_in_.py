"""remove chapter field in GeneralMultipleChoicesQuiz table

Revision ID: f6fa2f24b6a2
Revises: 4a6bb5728405
Create Date: 2022-02-04 14:42:13.436575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6fa2f24b6a2'
down_revision = '4a6bb5728405'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('general mulitple choices quiz', schema=None) as batch_op:
        batch_op.drop_index('ix_general mulitple choices quiz_chapter')
        batch_op.drop_column('chapter')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('general mulitple choices quiz', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chapter', sa.VARCHAR(length=64), nullable=True))
        batch_op.create_index('ix_general mulitple choices quiz_chapter', ['chapter'], unique=False)

    # ### end Alembic commands ###
