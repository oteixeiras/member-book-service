"""Initial migration

Revision ID: 46a0acb9e67e
Revises: 
Create Date: 2025-09-14 03:51:42.100934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46a0acb9e67e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create market_segmentation table
    op.create_table('market_segmentation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_market_segmentation_id'), 'market_segmentation', ['id'], unique=False)

    # Create addresses table
    op.create_table('addresses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('street', sa.String(), nullable=False),
        sa.Column('number', sa.String(), nullable=True),
        sa.Column('complement', sa.String(), nullable=True),
        sa.Column('neighborhood', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('state', sa.Enum('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO', name='stateenum'), nullable=False),
        sa.Column('country', sa.String(), nullable=False, server_default='Brazil'),
        sa.Column('postal_code', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_addresses_id'), 'addresses', ['id'], unique=False)

    # Create profiles table
    op.create_table('profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('eternity', 'infinity', 'admin', 'standalone_profile', name='profiletypeenum'), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('rule_activation', sa.JSON(), nullable=True),
        sa.Column('plan_price', sa.Integer(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profiles_id'), 'profiles', ['id'], unique=False)

    # Create companies table
    op.create_table('companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('market_segmentation_id', sa.Integer(), nullable=True),
        sa.Column('address_id', sa.Integer(), nullable=True),
        sa.Column('document', sa.String(), nullable=True),
        sa.Column('founded_year', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ),
        sa.ForeignKeyConstraint(['market_segmentation_id'], ['market_segmentation.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_companies_id'), 'companies', ['id'], unique=False)

    # Create members table
    op.create_table('members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('position', sa.String(), nullable=True),
        sa.Column('biography', sa.String(), nullable=True),
        sa.Column('document', sa.String(), nullable=True),
        sa.Column('photo_url', sa.String(), nullable=True),
        sa.Column('address_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'active', 'inactive', 'canceled', name='memberstatusenum'), nullable=True),
        sa.Column('expired_at', sa.Date(), nullable=True),
        sa.Column('profile_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_members_id'), 'members', ['id'], unique=False)

    # Create contact_channels table
    op.create_table('contact_channels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('whatsapp', 'email', 'instagram', 'linkedin', 'phone', 'others', name='contactchanneltypeenum'), nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('member_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contact_channels_id'), 'contact_channels', ['id'], unique=False)

    # Create additional_infos table
    op.create_table('additional_infos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=True),
        sa.Column('hobby', sa.String(), nullable=True),
        sa.Column('role_duration', sa.Integer(), nullable=True),
        sa.Column('children_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_additional_infos_id'), 'additional_infos', ['id'], unique=False)

    # Create performance table
    op.create_table('performance',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('count_closed_deals', sa.Integer(), nullable=True),
        sa.Column('value_closed_deals', sa.Integer(), nullable=True),
        sa.Column('referrals_received', sa.Integer(), nullable=True),
        sa.Column('total_value_per_referral', sa.Integer(), nullable=True),
        sa.Column('referrals_given', sa.Integer(), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_performance_id'), 'performance', ['id'], unique=False)

    # Create performance_events table
    op.create_table('performance_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('performance_id', sa.Integer(), nullable=True),
        sa.Column('event_id', sa.Integer(), nullable=True, autoincrement=True),
        sa.Column('type', sa.Enum('referral', 'transaction', name='performanceeventtypeenum'), nullable=False),
        sa.Column('value', sa.Integer(), nullable=True),
        sa.Column('member_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
        sa.ForeignKeyConstraint(['performance_id'], ['performance.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_performance_events_id'), 'performance_events', ['id'], unique=False)

    # Create members_companies table
    op.create_table('members_companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_members_companies_id'), 'members_companies', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_members_companies_id'), table_name='members_companies')
    op.drop_table('members_companies')
    op.drop_index(op.f('ix_performance_events_id'), table_name='performance_events')
    op.drop_table('performance_events')
    op.drop_index(op.f('ix_performance_id'), table_name='performance')
    op.drop_table('performance')
    op.drop_index(op.f('ix_additional_infos_id'), table_name='additional_infos')
    op.drop_table('additional_infos')
    op.drop_index(op.f('ix_contact_channels_id'), table_name='contact_channels')
    op.drop_table('contact_channels')
    op.drop_index(op.f('ix_members_id'), table_name='members')
    op.drop_table('members')
    op.drop_index(op.f('ix_companies_id'), table_name='companies')
    op.drop_table('companies')
    op.drop_index(op.f('ix_profiles_id'), table_name='profiles')
    op.drop_table('profiles')
    op.drop_index(op.f('ix_addresses_id'), table_name='addresses')
    op.drop_table('addresses')
    op.drop_index(op.f('ix_market_segmentation_id'), table_name='market_segmentation')
    op.drop_table('market_segmentation')
