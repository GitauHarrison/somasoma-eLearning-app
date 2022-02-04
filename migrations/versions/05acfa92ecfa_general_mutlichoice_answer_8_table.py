"""general mutlichoice answer 8 table

Revision ID: 05acfa92ecfa
Revises: caed385879dd
Create Date: 2022-02-04 07:01:50.020215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05acfa92ecfa'
down_revision = 'caed385879dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('general_multiple_choices_answer_8',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name=op.f('fk_general_multiple_choices_answer_8_student_id_student')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_general_multiple_choices_answer_8'))
    )
    with op.batch_alter_table('general_multiple_choices_answer_8', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_general_multiple_choices_answer_8_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('general_multiple_choices_answer_8', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_general_multiple_choices_answer_8_timestamp'))

    op.drop_table('general_multiple_choices_answer_8')
    # ### end Alembic commands ###
