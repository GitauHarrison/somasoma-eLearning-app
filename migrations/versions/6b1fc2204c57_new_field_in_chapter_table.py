"""new field in chapter table

Revision ID: 6b1fc2204c57
Revises: 5b623f622d1b
Create Date: 2022-01-20 18:33:12.392861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b1fc2204c57'
down_revision = '5b623f622d1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.add_column(sa.Column('overview_html', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.drop_column('overview_html')

    # ### end Alembic commands ###
