"""empty message

Revision ID: 7945cc08f1e1
Revises: 5caa5a27cdd7
Create Date: 2023-11-17 12:50:16.957872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7945cc08f1e1'
down_revision = '5caa5a27cdd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('petition_control',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_petition', sa.DateTime(timezone=150), nullable=False),
    sa.Column('process_affected', sa.String(length=100), nullable=False),
    sa.Column('name_customer', sa.String(length=100), nullable=False),
    sa.Column('process_customer', sa.String(length=100), nullable=False),
    sa.Column('date_petition_sent', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Enum('divulgado', 'distribuido', 'completado', name='status'), nullable=True),
    sa.Column('date_petition_received', sa.String(length=100), nullable=False),
    sa.Column('date_finished_petition', sa.String(length=100), nullable=False),
    sa.Column('observation', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('petition_control')
    # ### end Alembic commands ###