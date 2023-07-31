"""empty message

Revision ID: 04796eb73168
Revises: dd25d74456d4
Create Date: 2023-07-25 23:38:29.786073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04796eb73168'
down_revision = 'dd25d74456d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.drop_column('genres')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))

    # ### end Alembic commands ###