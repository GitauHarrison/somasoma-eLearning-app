"""general mutlichoice answer 10 table

Revision ID: 7903590ef087
Revises: bbc12bbd8a78
Create Date: 2022-02-04 07:06:10.402937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7903590ef087'
down_revision = 'bbc12bbd8a78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('general_multiple_choices_answer_10',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name=op.f('fk_general_multiple_choices_answer_10_student_id_student')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_general_multiple_choices_answer_10'))
    )
    with op.batch_alter_table('general_multiple_choices_answer_10', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_general_multiple_choices_answer_10_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('general_multiple_choices_answer_10', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_general_multiple_choices_answer_10_timestamp'))

    op.drop_table('general_multiple_choices_answer_10')
    # ### end Alembic commands ###