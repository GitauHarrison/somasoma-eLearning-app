"""teacher followers association table

Revision ID: aa5ba63f6c59
Revises: 33cb6fca6ffb
Create Date: 2021-12-28 07:03:49.905608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa5ba63f6c59'
down_revision = '33cb6fca6ffb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teacher_followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['teacher.id'], name=op.f('fk_teacher_followers_followed_id_teacher')),
    sa.ForeignKeyConstraint(['follower_id'], ['teacher.id'], name=op.f('fk_teacher_followers_follower_id_teacher'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher_followers')
    # ### end Alembic commands ###
