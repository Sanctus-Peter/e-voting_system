"""Create official table

Revision ID: 1b256f116464
Revises: e298a531f138
Create Date: 2023-02-27 15:49:35.507366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b256f116464'
down_revision = 'e298a531f138'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('officials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('reg_date', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('officials')
    # ### end Alembic commands ###