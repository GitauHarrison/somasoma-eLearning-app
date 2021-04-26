"""teacher table

Revision ID: b53db8b2f9b9
Revises: 876420c42d4e
Create Date: 2021-04-24 19:53:42.399856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b53db8b2f9b9'
down_revision = '876420c42d4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('verification_phone', sa.String(length=16), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teacher_email'), 'teacher', ['email'], unique=True)
    op.create_index(op.f('ix_teacher_first_name'), 'teacher', ['first_name'], unique=True)
    op.create_index(op.f('ix_teacher_last_name'), 'teacher', ['last_name'], unique=True)
    op.create_index(op.f('ix_teacher_username'), 'teacher', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_teacher_username'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_last_name'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_first_name'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_email'), table_name='teacher')
    op.drop_table('teacher')
    # ### end Alembic commands ###