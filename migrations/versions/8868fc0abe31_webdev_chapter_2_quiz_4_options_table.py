"""webdev chapter 2 quiz 4 options table

Revision ID: 8868fc0abe31
Revises: bebff957857b
Create Date: 2022-02-03 05:50:04.402783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8868fc0abe31'
down_revision = 'bebff957857b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('web_dev_chapter_2_quiz_4_options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name=op.f('fk_web_dev_chapter_2_quiz_4_options_student_id_student')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_web_dev_chapter_2_quiz_4_options'))
    )
    with op.batch_alter_table('web_dev_chapter_2_quiz_4_options', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_web_dev_chapter_2_quiz_4_options_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter_2_quiz_4_options', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_web_dev_chapter_2_quiz_4_options_timestamp'))

    op.drop_table('web_dev_chapter_2_quiz_4_options')
    # ### end Alembic commands ###
