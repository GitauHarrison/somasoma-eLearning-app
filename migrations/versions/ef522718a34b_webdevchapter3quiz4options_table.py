"""WebDevChapter3Quiz4Options table

Revision ID: ef522718a34b
Revises: c8016f2d8585
Create Date: 2022-02-03 12:55:54.727575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef522718a34b'
down_revision = 'c8016f2d8585'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('web_dev_chapter_3_quiz_4_options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name=op.f('fk_web_dev_chapter_3_quiz_4_options_student_id_student')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_web_dev_chapter_3_quiz_4_options'))
    )
    with op.batch_alter_table('web_dev_chapter_3_quiz_4_options', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_web_dev_chapter_3_quiz_4_options_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter_3_quiz_4_options', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_web_dev_chapter_3_quiz_4_options_timestamp'))

    op.drop_table('web_dev_chapter_3_quiz_4_options')
    # ### end Alembic commands ###
