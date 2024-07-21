"""Tornar a coluna protocol NOT NULL novamente

Revision ID: 5e70054a78eb
Revises: 57973d5f2ba7
Create Date: 2024-07-20 18:34:53.225807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e70054a78eb'
down_revision = '57973d5f2ba7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('solicitation', 'protocol',
                    existing_type=sa.String(length=20),
                    nullable=False)

def downgrade():
    op.alter_column('solicitation', 'protocol',
                    existing_type=sa.String(length=20),
                    nullable=True)