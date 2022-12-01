"""empty message

Revision ID: fe66dc1dd29f
Revises: 5ebc5ebfc306
Create Date: 2022-12-01 11:36:08.564821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe66dc1dd29f'
down_revision = '5ebc5ebfc306'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('taken', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'taken')
    # ### end Alembic commands ###
