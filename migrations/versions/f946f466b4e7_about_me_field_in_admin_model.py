"""about me field in admin model

Revision ID: f946f466b4e7
Revises: b010cb32b9c1
Create Date: 2021-12-26 04:15:37.070613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f946f466b4e7'
down_revision = 'b010cb32b9c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin_about_me', sa.String(length=140), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_column('admin_about_me')

    # ### end Alembic commands ###
