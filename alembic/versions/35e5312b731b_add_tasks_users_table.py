"""add tasks users table

Revision ID: 35e5312b731b
Revises: 06d9ca2508ae
Create Date: 2022-08-04 00:25:53.874509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35e5312b731b'
down_revision = '06d9ca2508ae'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tasks_users',
    sa.Column("task_id", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
    sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
    sa.PrimaryKeyConstraint(["task_id", "user_id"]),
    )


def downgrade():
    op.drop_table('tasks_users')
