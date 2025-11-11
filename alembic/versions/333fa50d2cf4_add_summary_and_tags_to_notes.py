from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '333fa50d2cf4'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('notes', sa.Column('summary', sa.String(length=255), nullable=True))
    op.add_column('notes', sa.Column('tags', postgresql.ARRAY(sa.String), nullable=True))

def downgrade() -> None:
    op.drop_column('notes', 'tags')
    op.drop_column('notes', 'summary')
