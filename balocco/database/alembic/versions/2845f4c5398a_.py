"""empty message

Revision ID: 2845f4c5398a
Revises: f4131cd513ea
Create Date: 2022-11-30 18:46:08.293042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2845f4c5398a'
down_revision = 'f4131cd513ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('giveaway', sa.Column('active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('giveaway', 'active')
    # ### end Alembic commands ###