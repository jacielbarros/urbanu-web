"""Add fields to User model

Revision ID: 94f0fa56d787
Revises: c925d05ad049
Create Date: 2024-06-16 10:11:21.503827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94f0fa56d787'
down_revision = 'c925d05ad049'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cpf', sa.String(length=11), nullable=False))
        batch_op.add_column(sa.Column('full_name', sa.String(length=128), nullable=False))
        batch_op.add_column(sa.Column('mobile_number', sa.String(length=20), nullable=False))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.drop_index('ix_user_email')
        batch_op.drop_index('ix_user_username')
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.create_unique_constraint(None, ['cpf'])
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('ix_user_username', ['username'], unique=True)
        batch_op.create_index('ix_user_email', ['email'], unique=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.drop_column('mobile_number')
        batch_op.drop_column('full_name')
        batch_op.drop_column('cpf')

    # ### end Alembic commands ###