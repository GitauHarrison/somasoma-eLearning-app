"""web dev chapter3 quiz total score

Revision ID: 00f001a958b1
Revises: b95f0132b231
Create Date: 2022-03-02 11:57:04.695611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00f001a958b1'
down_revision = 'b95f0132b231'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('web_dev_chapter3_quiz_total_score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_score', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name=op.f('fk_web_dev_chapter3_quiz_total_score_student_id_student')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_web_dev_chapter3_quiz_total_score'))
    )
    with op.batch_alter_table('web_dev_chapter3_quiz_total_score', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_web_dev_chapter3_quiz_total_score_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_web_dev_chapter3_quiz_total_score_total_score'), ['total_score'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_dev_chapter3_quiz_total_score', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_web_dev_chapter3_quiz_total_score_total_score'))
        batch_op.drop_index(batch_op.f('ix_web_dev_chapter3_quiz_total_score_timestamp'))

    op.drop_table('web_dev_chapter3_quiz_total_score')
    # ### end Alembic commands ###
