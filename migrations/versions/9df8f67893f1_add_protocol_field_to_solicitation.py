"""Add protocol field to solicitation

Revision ID: 9df8f67893f1
Revises: db6d67dca945
Create Date: 2024-07-20 11:50:30.550399

"""
from alembic import op
import sqlalchemy as sa

# Revisão e ID de downgrade
revision = '9df8f67893f1'
down_revision = 'db6d67dca945'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('solicitation', schema=None) as batch_op:
        batch_op.alter_column('protocol',
                              existing_type=sa.String(length=20),
                              nullable=False)

def downgrade():
    with op.batch_alter_table('solicitation', schema=None) as batch_op:
        batch_op.alter_column('protocol',
                              existing_type=sa.String(length=20),
                              nullable=True)




    # ### end Alembic commands ###
