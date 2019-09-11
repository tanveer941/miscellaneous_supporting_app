"""empty message

Revision ID: 1c85165c73f0
Revises: f066dd8fdaf
Create Date: 2019-08-18 08:13:21.828000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c85165c73f0'
down_revision = 'f066dd8fdaf'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('addr', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'addr')
    ### end Alembic commands ###
