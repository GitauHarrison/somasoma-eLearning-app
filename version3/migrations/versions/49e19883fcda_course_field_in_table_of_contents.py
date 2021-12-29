"""course field in table of contents

Revision ID: 49e19883fcda
Revises: 8951c53efcf4
Create Date: 2021-12-29 01:05:45.523196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49e19883fcda'
down_revision = '8951c53efcf4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('table of contents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course', sa.String(length=140), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('table of contents', schema=None) as batch_op:
        batch_op.drop_column('course')

    # ### end Alembic commands ###