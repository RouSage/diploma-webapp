"""Plot image path column added

Revision ID: 3f72f3e2635a
Revises: c9a5c84bec47
Create Date: 2019-05-11 14:39:30.390262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f72f3e2635a'
down_revision = 'c9a5c84bec47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('plot_path', sa.String(length=200), nullable=True))
    op.create_unique_constraint(None, 'image', ['plot_path'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'image', type_='unique')
    op.drop_column('image', 'plot_path')
    # ### end Alembic commands ###
