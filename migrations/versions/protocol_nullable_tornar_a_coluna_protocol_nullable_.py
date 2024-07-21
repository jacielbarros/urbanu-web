"""Tornar a coluna protocol nullable temporariamente

Revision ID: protocol_nullable
Revises: 4c1b1ffe4d93
Create Date: 2024-07-21 10:20:12.772046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'protocol_nullable'
down_revision = '4c1b1ffe4d93'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('solicitation', 'protocol', existing_type=sa.String(length=20), nullable=True)

def downgrade():
    op.alter_column('solicitation', 'protocol', existing_type=sa.String(length=20), nullable=False)