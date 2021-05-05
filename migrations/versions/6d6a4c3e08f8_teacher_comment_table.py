"""teacher comment table

Revision ID: 6d6a4c3e08f8
Revises: 01afa7565197
Create Date: 2021-05-05 14:07:27.296158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d6a4c3e08f8'
down_revision = '01afa7565197'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teacher_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=300), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], name=op.f('fk_teacher_comment_teacher_id_teacher')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_teacher_comment'))
    )
    with op.batch_alter_table('teacher_comment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_teacher_comment_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher_comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_teacher_comment_timestamp'))

    op.drop_table('teacher_comment')
    # ### end Alembic commands ###
