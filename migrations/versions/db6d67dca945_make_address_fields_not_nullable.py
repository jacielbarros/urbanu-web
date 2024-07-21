"""Make address fields not nullable

Revision ID: db6d67dca945
Revises: bf0d17ff1e6d
Create Date: 2024-07-19 21:14:50.611397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db6d67dca945'
down_revision = 'bf0d17ff1e6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('solicitation', schema=None) as batch_op:
        batch_op.alter_column('cep',
               existing_type=sa.VARCHAR(length=8),
               nullable=False)
        batch_op.alter_column('logradouro',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
        batch_op.alter_column('bairro',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('cidade',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('uf',
               existing_type=sa.VARCHAR(length=2),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('solicitation', schema=None) as batch_op:
        batch_op.alter_column('uf',
               existing_type=sa.VARCHAR(length=2),
               nullable=True)
        batch_op.alter_column('cidade',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('bairro',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('logradouro',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
        batch_op.alter_column('cep',
               existing_type=sa.VARCHAR(length=8),
               nullable=True)

    # ### end Alembic commands ###