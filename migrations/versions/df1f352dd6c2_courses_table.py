"""courses table

Revision ID: df1f352dd6c2
Revises: c2f53b276f42
Create Date: 2021-12-27 03:21:04.479236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df1f352dd6c2'
down_revision = 'c2f53b276f42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_image', sa.String(length=300), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('body', sa.String(length=300), nullable=True),
    sa.Column('overview', sa.String(length=300), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('next_class_date', sa.String(length=300), nullable=True),
    sa.Column('link', sa.String(length=300), nullable=True),
    sa.Column('allowed_status', sa.Boolean(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], name=op.f('fk_course_admin_id_admin')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_course'))
    )
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_course_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_course_title'), ['title'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_course_title'))
        batch_op.drop_index(batch_op.f('ix_course_timestamp'))

    op.drop_table('course')
    # ### end Alembic commands ###
