"""Atualiza campo protocol

Revision ID: ffd435902575
Revises: 48619f815863
Create Date: 2024-07-20 18:22:06.794349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffd435902575'
down_revision = '48619f815863'
branch_labels = None
depends_on = None


def upgrade():
    # Tornar a coluna 'protocol' NOT NULL
    op.alter_column('solicitation', 'protocol',
                    existing_type=sa.String(length=20),
                    nullable=False)
    # Garantir que a coluna 'protocol' seja única
    op.create_unique_constraint('uq_protocol', 'solicitation', ['protocol'])

def downgrade():
    # Reverter as mudanças, se necessário
    op.drop_constraint('uq_protocol', 'solicitation', type_='unique')
    op.alter_column('solicitation', 'protocol',
                    existing_type=sa.String(length=20),
                    nullable=True)