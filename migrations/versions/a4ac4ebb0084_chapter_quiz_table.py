"""chapter quiz table

Revision ID: a4ac4ebb0084
Revises: af3eabecc4e5
Create Date: 2021-12-30 12:44:14.236977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4ac4ebb0084'
down_revision = 'af3eabecc4e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chapter quiz',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course', sa.String(length=140), nullable=True),
    sa.Column('chapter', sa.String(length=64), nullable=True),
    sa.Column('review_quiz_link', sa.String(length=140), nullable=True),
    sa.Column('quiz_1', sa.String(length=140), nullable=True),
    sa.Column('quiz_2', sa.String(length=140), nullable=True),
    sa.Column('quiz_3', sa.String(length=140), nullable=True),
    sa.Column('quiz_4', sa.String(length=140), nullable=True),
    sa.Column('quiz_5', sa.String(length=140), nullable=True),
    sa.Column('allowed_status', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], name=op.f('fk_chapter quiz_teacher_id_teacher')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_chapter quiz'))
    )
    with op.batch_alter_table('chapter quiz', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_chapter quiz_chapter'), ['chapter'], unique=False)
        batch_op.create_index(batch_op.f('ix_chapter quiz_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter quiz', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_chapter quiz_timestamp'))
        batch_op.drop_index(batch_op.f('ix_chapter quiz_chapter'))

    op.drop_table('chapter quiz')
    # ### end Alembic commands ###
