"""table of contents table

Revision ID: 01e7b0f1bfd4
Revises: 439783bb7f69
Create Date: 2021-12-28 19:27:38.339059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01e7b0f1bfd4'
down_revision = '439783bb7f69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('table of contents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('chapter', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('allowed_status', sa.Boolean(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], name=op.f('fk_table of contents_teacher_id_teacher')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_table of contents'))
    )
    with op.batch_alter_table('table of contents', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_table of contents_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_table of contents_title'), ['title'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('table of contents', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_table of contents_title'))
        batch_op.drop_index(batch_op.f('ix_table of contents_timestamp'))

    op.drop_table('table of contents')
    # ### end Alembic commands ###
