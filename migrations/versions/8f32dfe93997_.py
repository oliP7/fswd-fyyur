"""empty message

Revision ID: 8f32dfe93997
Revises: 548d65fd68ba
Create Date: 2023-07-22 01:54:07.674623

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8f32dfe93997'
down_revision = '548d65fd68ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('music_genres',
               existing_type=postgresql.ARRAY(postgresql.ENUM('ALTERNATIVE', 'BLUES', 'CLASSICAL', 'COUNTRY', 'ELECTRONIC', 'FOLK', 'FUNK', 'HIP_HOP', 'HEAVY_METAL', 'INSTRUMENTAL', 'JAZZ', 'THEATRE', 'POP', 'PUNK', 'R_AND_B', 'REGGAE', 'ROCK_N_ROLL', 'SOUL', 'OTHER', name='musictypes')),
               type_=sa.ARRAY(sa.String(length=120)),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('music_genres',
               existing_type=sa.ARRAY(sa.String(length=120)),
               type_=postgresql.ARRAY(postgresql.ENUM('ALTERNATIVE', 'BLUES', 'CLASSICAL', 'COUNTRY', 'ELECTRONIC', 'FOLK', 'FUNK', 'HIP_HOP', 'HEAVY_METAL', 'INSTRUMENTAL', 'JAZZ', 'THEATRE', 'POP', 'PUNK', 'R_AND_B', 'REGGAE', 'ROCK_N_ROLL', 'SOUL', 'OTHER', name='musictypes')),
               existing_nullable=True)

    # ### end Alembic commands ###
