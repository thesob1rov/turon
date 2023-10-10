"""empty message

Revision ID: d700966dcde7
Revises: 2803a261e851
Create Date: 2023-09-06 22:41:01.686525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd700966dcde7'
down_revision = '2803a261e851'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('time_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lesson_count', sa.Integer(), nullable=True),
    sa.Column('start', sa.String(), nullable=True),
    sa.Column('end', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('flow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('chair_count', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('daily_time',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('flow_id', sa.Integer(), nullable=True),
    sa.Column('day_of_the_week', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['flow_id'], ['flow.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('flow_students',
    sa.Column('flow_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['flow_id'], ['flow.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flow_students')
    op.drop_table('daily_time')
    op.drop_table('room')
    op.drop_table('flow')
    op.drop_table('time_list')
    # ### end Alembic commands ###
