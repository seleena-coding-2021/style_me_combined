"""Initial

Revision ID: 92b39f84f6dd
Revises: 
Create Date: 2022-10-07 21:55:33.634199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92b39f84f6dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('style',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_name', sa.String(length=100), nullable=False),
    sa.Column('stylechoice', sa.String(length=100), nullable=True),
    sa.Column('season', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('image_name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('zipcode', sa.String(length=100), nullable=True),
    sa.Column('birthday', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('style')
    # ### end Alembic commands ###
