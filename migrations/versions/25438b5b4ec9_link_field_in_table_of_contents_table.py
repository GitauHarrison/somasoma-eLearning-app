"""link field in table of contents table

Revision ID: 25438b5b4ec9
Revises: 01e7b0f1bfd4
Create Date: 2021-12-28 19:48:46.900115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25438b5b4ec9'
down_revision = '01e7b0f1bfd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('table of contents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('link', sa.String(length=140), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('table of contents', schema=None) as batch_op:
        batch_op.drop_column('link')

    # ### end Alembic commands ###
