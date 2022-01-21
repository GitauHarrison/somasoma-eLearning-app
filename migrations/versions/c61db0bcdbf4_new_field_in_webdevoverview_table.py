"""new field in webdevoverview table

Revision ID: c61db0bcdbf4
Revises: 6b1fc2204c57
Create Date: 2022-01-20 18:34:34.481565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c61db0bcdbf4'
down_revision = '6b1fc2204c57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web development overview', schema=None) as batch_op:
        batch_op.add_column(sa.Column('overview_html', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web development overview', schema=None) as batch_op:
        batch_op.drop_column('overview_html')

    # ### end Alembic commands ###