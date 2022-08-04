"""add projects table

Revision ID: f1424de56223
Revises: bdbce349c5c9
Create Date: 2022-08-04 00:15:18.406206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1424de56223'
down_revision = 'bdbce349c5c9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('description', sa.String(length=1024), nullable=False),
    sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
    sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f('ix_projects_title'), 'projects', ['title'], unique=False)
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_index(op.f('ix_projects_title'), table_name='projects')
    op.drop_table('projects')
