"""webdev chapter 2 comment table

Revision ID: 7101f488e0b5
Revises: 338d202f7dee
Create Date: 2022-02-02 19:24:50.553162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7101f488e0b5'
down_revision = '338d202f7dee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chapter 2 comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.Column('allowed_status', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name=op.f('fk_chapter 2 comment_student_id_student')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_chapter 2 comment'))
    )
    with op.batch_alter_table('chapter 2 comment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_chapter 2 comment_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter 2 comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_chapter 2 comment_timestamp'))

    op.drop_table('chapter 2 comment')
    # ### end Alembic commands ###
