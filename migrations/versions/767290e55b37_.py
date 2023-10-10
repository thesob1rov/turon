"""empty message

Revision ID: 767290e55b37
Revises: e7757883275d
Create Date: 2023-08-28 18:13:57.020601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '767290e55b37'
down_revision = 'e7757883275d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'class_type', ['class_number'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
