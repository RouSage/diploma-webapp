"""Db structure

Revision ID: 4aa1cbccf7f0
Revises: 
Create Date: 2019-06-01 12:36:07.605109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4aa1cbccf7f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=200), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_path'), 'image', ['path'], unique=True)
    op.create_table('plot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=200), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.create_table('prediction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('probability', sa.Float(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prediction')
    op.drop_table('plot')
    op.drop_index(op.f('ix_image_path'), table_name='image')
    op.drop_table('image')
    op.drop_table('classes')
    # ### end Alembic commands ###
