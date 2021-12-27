"""timestamp field in blog articles model

Revision ID: a1d82b689d6e
Revises: e78122dde5e1
Create Date: 2021-12-27 06:59:22.857499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1d82b689d6e'
down_revision = 'e78122dde5e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_blog articles_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog articles', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_blog articles_timestamp'))
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###