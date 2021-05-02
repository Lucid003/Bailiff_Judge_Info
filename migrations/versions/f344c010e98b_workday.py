"""workday

Revision ID: f344c010e98b
Revises: 7266ba14494d
Create Date: 2021-05-02 21:18:07.588916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f344c010e98b'
down_revision = '7266ba14494d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workday',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('weekday', sa.String(length=9), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('data', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workday')
    # ### end Alembic commands ###
