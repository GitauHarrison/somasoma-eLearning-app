"""allowed status field blog artilces

Revision ID: aa2aa87a965d
Revises: ee8f9a6b7d21
Create Date: 2021-12-27 11:57:33.778604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa2aa87a965d'
down_revision = 'ee8f9a6b7d21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('allowed_status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog articles', schema=None) as batch_op:
        batch_op.drop_column('allowed_status')

    # ### end Alembic commands ###
