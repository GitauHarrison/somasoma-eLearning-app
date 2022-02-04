"""WebDevChapter3Quiz2Options table

Revision ID: 4b00c4ba96eb
Revises: 8c9ceb1c2db0
Create Date: 2022-02-03 12:50:42.583857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b00c4ba96eb'
down_revision = '8c9ceb1c2db0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('web_dev_chapter_3_quiz_2_options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name=op.f('fk_web_dev_chapter_3_quiz_2_options_student_id_student')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_web_dev_chapter_3_quiz_2_options'))
    )
    with op.batch_alter_table('web_dev_chapter_3_quiz_2_options', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_web_dev_chapter_3_quiz_2_options_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter_3_quiz_2_options', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_web_dev_chapter_3_quiz_2_options_timestamp'))

    op.drop_table('web_dev_chapter_3_quiz_2_options')
    # ### end Alembic commands ###