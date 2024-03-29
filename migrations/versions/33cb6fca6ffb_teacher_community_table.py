"""teacher community table

Revision ID: 33cb6fca6ffb
Revises: 1e5e23e8cbfc
Create Date: 2021-12-28 05:58:53.401189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33cb6fca6ffb'
down_revision = '1e5e23e8cbfc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teacher community comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], name=op.f('fk_teacher community comment_teacher_id_teacher')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_teacher community comment'))
    )
    with op.batch_alter_table('teacher community comment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_teacher community comment_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher community comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_teacher community comment_timestamp'))

    op.drop_table('teacher community comment')
    # ### end Alembic commands ###
