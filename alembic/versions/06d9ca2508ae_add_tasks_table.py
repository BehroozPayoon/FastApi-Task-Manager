"""add tasks table

Revision ID: 06d9ca2508ae
Revises: f1424de56223
Create Date: 2022-08-04 00:21:28.327728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06d9ca2508ae'
down_revision = 'f1424de56223'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column("project_id", sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=False, unique=True),
    sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
    sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f('ix_tasks_title'), 'tasks', ['title'], unique=False)
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_title'), table_name='tasks')
    op.drop_table('tasks')
