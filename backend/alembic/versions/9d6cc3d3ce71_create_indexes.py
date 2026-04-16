"""create indexes

Revision ID: 9d6cc3d3ce71
Revises: a4553ff8bdb5
Create Date: 2026-04-16 18:29:43.528047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d6cc3d3ce71'
down_revision: Union[str, Sequence[str], None] = 'a4553ff8bdb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    media_type = sa.Enum("movie", "tv", name="media_type")
    media_type.create(op.get_bind())

    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.create_unique_constraint(None, 'users', ['username'])

    op.add_column('watchlist_items', sa.Column('tmdb_id', sa.Integer(), nullable=False))
    op.add_column('watchlist_items', sa.Column('notes', sa.Text(), nullable=True))
    op.add_column('watchlist_items', sa.Column('rating', sa.Integer(), nullable=True))
    op.add_column('watchlist_items', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('watchlist_items', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))

    op.alter_column('watchlist_items', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)

    op.alter_column('watchlist_items', 'type',
               existing_type=sa.VARCHAR(),
               type_=media_type,
               nullable=False,
               postgresql_using="type::media_type")

    op.alter_column('watchlist_items', 'watchlist_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    op.create_unique_constraint('uq_watchlist_tmdb', 'watchlist_items', ['watchlist_id', 'tmdb_id'])

    op.add_column('watchlists', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('watchlists', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f('ix_watchlists_user_id'), 'watchlists', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        'watchlist_items',
        'type',
        existing_type=sa.Enum('movie', 'tv', name='media_type'),
        type_=sa.VARCHAR(),
        postgresql_using="type::text",
        nullable=True
    )

    media_type = sa.Enum("movie", "tv", name="media_type")
    media_type.drop(op.get_bind())

    # rest of rollback
    op.drop_index(op.f('ix_watchlists_user_id'), table_name='watchlists')

    op.drop_column('watchlists', 'updated_at')
    op.drop_column('watchlists', 'created_at')

    op.drop_constraint('uq_watchlist_tmdb', 'watchlist_items', type_='unique')

    op.drop_column('watchlist_items', 'updated_at')
    op.drop_column('watchlist_items', 'created_at')
    op.drop_column('watchlist_items', 'rating')
    op.drop_column('watchlist_items', 'notes')
    op.drop_column('watchlist_items', 'tmdb_id')

    op.alter_column(
        'watchlist_items',
        'watchlist_id',
        existing_type=sa.INTEGER(),
        nullable=True
    )

    op.alter_column(
        'watchlist_items',
        'title',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.drop_constraint(None, 'users', type_='unique')

    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'username')