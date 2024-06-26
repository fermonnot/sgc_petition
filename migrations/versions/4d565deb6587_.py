"""empty message

Revision ID: 4d565deb6587
Revises: 940532a83611
Create Date: 2024-01-23 18:15:59.880194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d565deb6587'
down_revision = '940532a83611'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('petitions', schema=None) as batch_op:
        batch_op.alter_column('change_description',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=5000),
               existing_nullable=False)
        batch_op.alter_column('change_justify',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=5000),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('petitions', schema=None) as batch_op:
        batch_op.alter_column('change_justify',
               existing_type=sa.String(length=5000),
               type_=sa.VARCHAR(length=150),
               existing_nullable=False)
        batch_op.alter_column('change_description',
               existing_type=sa.String(length=5000),
               type_=sa.VARCHAR(length=150),
               existing_nullable=False)

    # ### end Alembic commands ###
