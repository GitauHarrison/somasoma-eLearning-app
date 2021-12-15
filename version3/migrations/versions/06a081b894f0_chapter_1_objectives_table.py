"""chapter 1 objectives table

Revision ID: 06a081b894f0
Revises: dc6bffeaff66
Create Date: 2021-12-15 09:18:35.215223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06a081b894f0'
down_revision = 'dc6bffeaff66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chapter1_objectives',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('objective_1', sa.Boolean(), nullable=True),
    sa.Column('objective_2', sa.Boolean(), nullable=True),
    sa.Column('objective_3', sa.Boolean(), nullable=True),
    sa.Column('objective_4', sa.Boolean(), nullable=True),
    sa.Column('objective_5', sa.Boolean(), nullable=True),
    sa.Column('objective_6', sa.Boolean(), nullable=True),
    sa.Column('objective_7', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chapter1_objectives_timestamp'), 'chapter1_objectives', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_chapter1_objectives_timestamp'), table_name='chapter1_objectives')
    op.drop_table('chapter1_objectives')
    # ### end Alembic commands ###