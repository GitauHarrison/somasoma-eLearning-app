"""unique constraint in email field flask stories table

Revision ID: 143989b39c2d
Revises: d733ecc9e3f0
Create Date: 2021-12-27 17:03:25.136100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '143989b39c2d'
down_revision = 'd733ecc9e3f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flask student stories', schema=None) as batch_op:
        batch_op.drop_index('ix_flask student stories_email')
        batch_op.create_unique_constraint(batch_op.f('uq_flask student stories_email'), ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flask student stories', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_flask student stories_email'), type_='unique')
        batch_op.create_index('ix_flask student stories_email', ['email'], unique=False)

    # ### end Alembic commands ###