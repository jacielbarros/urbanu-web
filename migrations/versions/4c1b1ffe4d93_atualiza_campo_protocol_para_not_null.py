"""Atualiza campo protocol para NOT NULL

Revision ID: 4c1b1ffe4d93
Revises: 888ab0f16cf3
Create Date: 2024-07-21 09:23:55.290674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c1b1ffe4d93'
down_revision = '888ab0f16cf3'
branch_labels = None
depends_on = None


def upgrade():
    # Tornar a coluna 'protocol' NOT NULL novamente
    op.alter_column('solicitation', 'protocol',
                    existing_type=sa.String(length=20),
                    nullable=False)

def downgrade():
    # Reverter a mudança para nullable
    op.alter_column('solicitation', 'protocol',
                    existing_type=sa.String(length=20),
                    nullable=True)