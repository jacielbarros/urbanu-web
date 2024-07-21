"""Add address fields to solicitation

Revision ID: bf0d17ff1e6d
Revises: c5c71219f764
Create Date: 2024-07-19 21:06:26.109126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf0d17ff1e6d'
down_revision = 'c5c71219f764'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('solicitation', schema=None) as batch_op:
        batch_op.alter_column('cep', existing_type=sa.String(length=8), nullable=False)
        batch_op.alter_column('logradouro', existing_type=sa.String(length=150), nullable=False)
        batch_op.alter_column('bairro', existing_type=sa.String(length=100), nullable=False)
        batch_op.alter_column('cidade', existing_type=sa.String(length=100), nullable=False)
        batch_op.alter_column('uf', existing_type=sa.String(length=2), nullable=False)

def downgrade():
    with op.batch_alter_table('solicitation', schema=None) as batch_op:
        batch_op.alter_column('cep', existing_type=sa.String(length=8), nullable=True)
        batch_op.alter_column('logradouro', existing_type=sa.String(length=150), nullable=True)
        batch_op.alter_column('bairro', existing_type=sa.String(length=100), nullable=True)
        batch_op.alter_column('cidade', existing_type=sa.String(length=100), nullable=True)
        batch_op.alter_column('uf', existing_type=sa.String(length=2), nullable=True)



    # ### end Alembic commands ###
