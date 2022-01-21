"""teacher manages blog article table

Revision ID: 742634e1bfb5
Revises: b876334e8f6a
Create Date: 2022-01-17 16:06:13.364248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '742634e1bfb5'
down_revision = 'b876334e8f6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('article_image', sa.String(length=140), nullable=True),
    sa.Column('article_name', sa.String(length=140), nullable=True),
    sa.Column('body', sa.String(length=300), nullable=True),
    sa.Column('link', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('allowed_status', sa.Boolean(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], name=op.f('fk_blog_articles_teacher_id_teacher')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_blog_articles'))
    )
    with op.batch_alter_table('blog_articles', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_blog_articles_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('blog articles', schema=None) as batch_op:
        batch_op.drop_index('ix_blog articles_timestamp')

    op.drop_table('blog articles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog articles',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('article_name', sa.VARCHAR(length=140), nullable=True),
    sa.Column('link', sa.VARCHAR(length=140), nullable=True),
    sa.Column('admin_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('article_image', sa.VARCHAR(length=140), nullable=True),
    sa.Column('body', sa.VARCHAR(length=300), nullable=True),
    sa.Column('allowed_status', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('blog articles', schema=None) as batch_op:
        batch_op.create_index('ix_blog articles_timestamp', ['timestamp'], unique=False)

    with op.batch_alter_table('blog_articles', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_blog_articles_timestamp'))

    op.drop_table('blog_articles')
    # ### end Alembic commands ###