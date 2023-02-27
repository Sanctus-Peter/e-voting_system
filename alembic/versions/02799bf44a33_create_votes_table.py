"""Create votes table

Revision ID: 02799bf44a33
Revises: 199e1f1bb583
Create Date: 2023-02-27 11:39:51.368751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02799bf44a33'
down_revision = '199e1f1bb583'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('voterId', sa.Integer(), nullable=False),
    sa.Column('electionId', sa.Integer(), nullable=False),
    sa.Column('voted_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('Now()'), nullable=False),
    sa.PrimaryKeyConstraint('voterId', 'electionId')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
