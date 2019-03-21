"""Added URL mapper table

Revision ID: b3e9d4be4d7c
Revises: 
Create Date: 2019-03-21 10:48:48.470261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b3e9d4be4d7c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "url_mapper",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("url", sa.String, nullable=False),
        sa.Column("path", sa.String, nullable=False),
        sa.Column("custom", sa.Boolean, nullable=False),
        sa.Column("created_on", sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table("url_mapper")
