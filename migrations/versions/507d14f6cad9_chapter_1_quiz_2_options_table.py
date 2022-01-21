"""chapter 1 quiz 2 options table

Revision ID: 507d14f6cad9
Revises: d269621317af
Create Date: 2022-01-12 10:12:45.079170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '507d14f6cad9'
down_revision = 'd269621317af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('web_dev_chapter_1_quiz_2_options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('option_1', sa.Boolean(), nullable=True),
    sa.Column('option_2', sa.Boolean(), nullable=True),
    sa.Column('option_3', sa.Boolean(), nullable=True),
    sa.Column('option_4', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name=op.f('fk_web_dev_chapter_1_quiz_2_options_student_id_student')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_web_dev_chapter_1_quiz_2_options'))
    )
    with op.batch_alter_table('web_dev_chapter_1_quiz_2_options', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_web_dev_chapter_1_quiz_2_options_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter_1_quiz_2_options', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_web_dev_chapter_1_quiz_2_options_timestamp'))

    op.drop_table('web_dev_chapter_1_quiz_2_options')
    # ### end Alembic commands ###