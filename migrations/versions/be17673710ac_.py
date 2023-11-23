"""empty message

Revision ID: be17673710ac
Revises: d60fa2c094b0
Create Date: 2023-11-23 15:52:06.431796

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'be17673710ac'
down_revision = 'd60fa2c094b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('petition_control', schema=None) as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)

    with op.batch_alter_table('petitions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('p_created', sa.DateTime(timezone=True), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('petitions', schema=None) as batch_op:
        batch_op.drop_column('p_created')

    with op.batch_alter_table('petition_control', schema=None) as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)

    # ### end Alembic commands ###
