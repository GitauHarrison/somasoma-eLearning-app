"""new field in events table

Revision ID: 5b623f622d1b
Revises: db2f057c9bf6
Create Date: 2022-01-20 18:30:34.071595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b623f622d1b'
down_revision = 'db2f057c9bf6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('body_html', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_column('body_html')

    # ### end Alembic commands ###