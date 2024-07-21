"""Tornar a coluna protocol NOT NULL novamente

Revision ID: 888ab0f16cf3
Revises: 5e70054a78eb
Create Date: 2024-07-21 09:16:08.722790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '888ab0f16cf3'
down_revision = '5e70054a78eb'
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