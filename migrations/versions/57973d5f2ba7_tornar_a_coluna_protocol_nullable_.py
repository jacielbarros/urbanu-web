"""Tornar a coluna protocol nullable temporariamente

Revision ID: 57973d5f2ba7
Revises: ffd435902575
Create Date: 2024-07-20 18:30:17.416989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57973d5f2ba7'
down_revision = 'ffd435902575'
branch_labels = None
depends_on = None


def upgrade():
    # Tornar a coluna 'protocol' NULLABLE temporariamente
    op.alter_column('solicitation', 'protocol',
                    existing_type=sa.String(length=20),
                    nullable=True)

def downgrade():
    # Reverter as mudanças, se necessário
    op.alter_column('solicitation', 'protocol',
                    existing_type=sa.String(length=20),
                    nullable=False)