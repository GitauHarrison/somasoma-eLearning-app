"""student table

Revision ID: 876420c42d4e
Revises: 7d4f0fa64901
Create Date: 2021-04-24 19:53:00.336870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '876420c42d4e'
down_revision = '7d4f0fa64901'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('verification_phone', sa.String(length=16), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_email'), 'student', ['email'], unique=True)
    op.create_index(op.f('ix_student_first_name'), 'student', ['first_name'], unique=True)
    op.create_index(op.f('ix_student_last_name'), 'student', ['last_name'], unique=True)
    op.create_index(op.f('ix_student_username'), 'student', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_student_username'), table_name='student')
    op.drop_index(op.f('ix_student_last_name'), table_name='student')
    op.drop_index(op.f('ix_student_first_name'), table_name='student')
    op.drop_index(op.f('ix_student_email'), table_name='student')
    op.drop_table('student')
    # ### end Alembic commands ###