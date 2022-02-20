"""add table page

Revision ID: b0ac4c477cb5
Revises: 
Create Date: 2022-02-20 20:19:12.828211

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b0ac4c477cb5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pages',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('url', sa.Text(), nullable=False, unique=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('hash', sa.Text(), nullable=True),
        sa.Column('mime_type', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('url'),
    )


def downgrade():
    op.drop_table('pages')
