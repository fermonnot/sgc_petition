"""empty message

Revision ID: dfecfb8ecc89
Revises: 7945cc08f1e1
Create Date: 2023-11-22 10:03:12.032579

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dfecfb8ecc89'
down_revision = '7945cc08f1e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('petition_control', schema=None) as batch_op:
        batch_op.alter_column('date_petition',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('petition_control', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('date_petition',
               existing_type=sa.DateTime(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_nullable=False)

    # ### end Alembic commands ###
