"""Add image field to solicitation

Revision ID: 17ce48da4004
Revises: 9df8f67893f1
Create Date: 2024-07-20 15:45:50.379093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17ce48da4004'
down_revision = '9df8f67893f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('solicitation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=255), nullable=True))
        batch_op.alter_column('protocol',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
        batch_op.create_unique_constraint(None, ['protocol'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('solicitation', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('protocol',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.drop_column('image')

    # ### end Alembic commands ###