"""delete overview column

Revision ID: 1627a77a0e55
Revises: 2df58a536956
Create Date: 2022-01-17 17:35:23.377969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1627a77a0e55'
down_revision = '2df58a536956'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_column('overview')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('overview', sa.VARCHAR(length=300), nullable=True))

    # ### end Alembic commands ###