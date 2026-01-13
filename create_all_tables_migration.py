"""
Database migration script to create all new tables for the dashboard features.

Run this script to create all the new tables needed for:
- Users & Roles (RBAC)
- Handoff & SLA
- Notifications
- Security (2FA, API keys, audit logs)
- Sales & Products
- Onboarding

Usage:
    python create_all_tables_migration.py
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set")
    sys.exit(1)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# SQL statements to create all new tables
MIGRATION_SQL = """
-- ========== USERS & ROLES TABLES ==========

CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id),
    name VARCHAR NOT NULL,
    description TEXT,
    is_system BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_roles_business_id ON roles(business_id);
CREATE INDEX IF NOT EXISTS idx_roles_name ON roles(name);

CREATE TABLE IF NOT EXISTS permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_permissions_name ON permissions(name);
CREATE INDEX IF NOT EXISTS idx_permissions_category ON permissions(category);

CREATE TABLE IF NOT EXISTS role_permissions (
    id SERIAL PRIMARY KEY,
    role_id INTEGER REFERENCES roles(id) NOT NULL,
    permission_id INTEGER REFERENCES permissions(id) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_role_permissions_role_id ON role_permissions(role_id);
CREATE INDEX IF NOT EXISTS idx_role_permissions_permission_id ON role_permissions(permission_id);

CREATE TABLE IF NOT EXISTS user_roles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    role_id INTEGER REFERENCES roles(id) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_role_id ON user_roles(role_id);

-- ========== HANDOFF TABLES ==========

CREATE TABLE IF NOT EXISTS handoffs (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    conversation_id INTEGER REFERENCES conversations(id) NOT NULL,
    assigned_to_user_id INTEGER REFERENCES users(id),
    status VARCHAR DEFAULT 'pending' NOT NULL,
    priority VARCHAR DEFAULT 'medium' NOT NULL,
    reason TEXT,
    assigned_at TIMESTAMP WITHOUT TIME ZONE,
    resolved_at TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_handoffs_business_id ON handoffs(business_id);
CREATE INDEX IF NOT EXISTS idx_handoffs_conversation_id ON handoffs(conversation_id);
CREATE INDEX IF NOT EXISTS idx_handoffs_assigned_to_user_id ON handoffs(assigned_to_user_id);
CREATE INDEX IF NOT EXISTS idx_handoffs_status ON handoffs(status);
CREATE INDEX IF NOT EXISTS idx_handoffs_priority ON handoffs(priority);
CREATE INDEX IF NOT EXISTS idx_handoffs_created_at ON handoffs(created_at);

CREATE TABLE IF NOT EXISTS slas (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    handoff_id INTEGER REFERENCES handoffs(id) NOT NULL,
    target_response_time INTEGER,
    target_resolution_time INTEGER,
    actual_response_time INTEGER,
    actual_resolution_time INTEGER,
    response_time_breached BOOLEAN DEFAULT FALSE NOT NULL,
    resolution_time_breached BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_slas_business_id ON slas(business_id);
CREATE INDEX IF NOT EXISTS idx_slas_handoff_id ON slas(handoff_id);

CREATE TABLE IF NOT EXISTS escalations (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    handoff_id INTEGER REFERENCES handoffs(id) NOT NULL,
    from_user_id INTEGER REFERENCES users(id),
    to_user_id INTEGER REFERENCES users(id),
    reason TEXT,
    escalated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    resolved_at TIMESTAMP WITHOUT TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_escalations_business_id ON escalations(business_id);
CREATE INDEX IF NOT EXISTS idx_escalations_handoff_id ON escalations(handoff_id);

-- ========== NOTIFICATIONS TABLES ==========

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id),
    user_id INTEGER REFERENCES users(id) NOT NULL,
    type VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    message TEXT NOT NULL,
    category VARCHAR,
    is_read BOOLEAN DEFAULT FALSE NOT NULL,
    read_at TIMESTAMP WITHOUT TIME ZONE,
    action_url VARCHAR,
    extra_data TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_notifications_business_id ON notifications(business_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications(type);
CREATE INDEX IF NOT EXISTS idx_notifications_category ON notifications(category);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);

CREATE TABLE IF NOT EXISTS notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    category VARCHAR NOT NULL,
    email_enabled BOOLEAN DEFAULT TRUE NOT NULL,
    in_app_enabled BOOLEAN DEFAULT TRUE NOT NULL,
    sms_enabled BOOLEAN DEFAULT FALSE NOT NULL,
    quiet_hours_start VARCHAR,
    quiet_hours_end VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_notification_preferences_user_id ON notification_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_notification_preferences_category ON notification_preferences(category);

-- ========== SECURITY TABLES ==========

CREATE TABLE IF NOT EXISTS two_factor_auth (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE NOT NULL,
    secret VARCHAR NOT NULL,
    is_enabled BOOLEAN DEFAULT FALSE NOT NULL,
    backup_codes TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_two_factor_auth_user_id ON two_factor_auth(user_id);

CREATE TABLE IF NOT EXISTS ip_allowlists (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    ip_address VARCHAR NOT NULL,
    description VARCHAR,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    created_by_user_id INTEGER REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_ip_allowlists_business_id ON ip_allowlists(business_id);
CREATE INDEX IF NOT EXISTS idx_ip_allowlists_ip_address ON ip_allowlists(ip_address);

CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    session_token VARCHAR UNIQUE NOT NULL,
    ip_address VARCHAR,
    user_agent VARCHAR,
    expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    last_activity TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_session_token ON sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);

CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    name VARCHAR NOT NULL,
    key_hash VARCHAR UNIQUE NOT NULL,
    permissions TEXT,
    last_used_at TIMESTAMP WITHOUT TIME ZONE,
    expires_at TIMESTAMP WITHOUT TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_api_keys_business_id ON api_keys(business_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX IF NOT EXISTS idx_api_keys_expires_at ON api_keys(expires_at);

CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id),
    user_id INTEGER REFERENCES users(id),
    action VARCHAR NOT NULL,
    resource_type VARCHAR,
    resource_id INTEGER,
    ip_address VARCHAR,
    user_agent VARCHAR,
    details TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_business_id ON audit_logs(business_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource_type ON audit_logs(resource_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- ========== SALES & PRODUCTS TABLES ==========

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    name VARCHAR NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    currency VARCHAR DEFAULT 'USD' NOT NULL,
    category VARCHAR,
    tags TEXT,
    image_url VARCHAR,
    inventory_count INTEGER,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_products_business_id ON products(business_id);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

CREATE TABLE IF NOT EXISTS digital_assets (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    name VARCHAR NOT NULL,
    description TEXT,
    file_url VARCHAR NOT NULL,
    file_size INTEGER,
    file_type VARCHAR,
    download_count INTEGER DEFAULT 0 NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_digital_assets_business_id ON digital_assets(business_id);

CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    name VARCHAR NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    currency VARCHAR DEFAULT 'USD' NOT NULL,
    duration INTEGER,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_services_business_id ON services(business_id);
CREATE INDEX IF NOT EXISTS idx_services_name ON services(name);

CREATE TABLE IF NOT EXISTS bundles (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    name VARCHAR NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    currency VARCHAR DEFAULT 'USD' NOT NULL,
    discount_percentage FLOAT,
    product_ids TEXT,
    service_ids TEXT,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_bundles_business_id ON bundles(business_id);
CREATE INDEX IF NOT EXISTS idx_bundles_name ON bundles(name);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    conversation_id INTEGER REFERENCES conversations(id),
    lead_id INTEGER REFERENCES leads(id),
    customer_name VARCHAR,
    customer_email VARCHAR,
    customer_phone VARCHAR,
    status VARCHAR DEFAULT 'pending' NOT NULL,
    total_amount FLOAT NOT NULL,
    currency VARCHAR DEFAULT 'USD' NOT NULL,
    payment_status VARCHAR DEFAULT 'pending' NOT NULL,
    payment_method VARCHAR,
    shipping_address TEXT,
    notes TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_orders_business_id ON orders(business_id);
CREATE INDEX IF NOT EXISTS idx_orders_conversation_id ON orders(conversation_id);
CREATE INDEX IF NOT EXISTS idx_orders_lead_id ON orders(lead_id);
CREATE INDEX IF NOT EXISTS idx_orders_customer_email ON orders(customer_email);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_payment_status ON orders(payment_status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) NOT NULL,
    product_id INTEGER REFERENCES products(id),
    service_id INTEGER REFERENCES services(id),
    bundle_id INTEGER REFERENCES bundles(id),
    item_type VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price FLOAT NOT NULL,
    total_price FLOAT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);

-- ========== ONBOARDING TABLES ==========

CREATE TABLE IF NOT EXISTS onboarding_steps (
    id SERIAL PRIMARY KEY,
    step_key VARCHAR UNIQUE NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT,
    "order" INTEGER NOT NULL,
    is_required BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_onboarding_steps_step_key ON onboarding_steps(step_key);

CREATE TABLE IF NOT EXISTS onboarding_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    business_id INTEGER REFERENCES businesses(id) NOT NULL,
    step_key VARCHAR NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE NOT NULL,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_onboarding_progress_user_id ON onboarding_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_onboarding_progress_business_id ON onboarding_progress(business_id);
CREATE INDEX IF NOT EXISTS idx_onboarding_progress_step_key ON onboarding_progress(step_key);

-- ========== INSERT DEFAULT DATA ==========

-- Insert default permissions
INSERT INTO permissions (name, description, category) VALUES
    ('conversations.view', 'View conversations', 'conversations'),
    ('conversations.manage', 'Manage conversations', 'conversations'),
    ('users.view', 'View users', 'users'),
    ('users.manage', 'Manage users', 'users'),
    ('settings.view', 'View settings', 'settings'),
    ('settings.manage', 'Manage settings', 'settings'),
    ('analytics.view', 'View analytics', 'analytics'),
    ('knowledge.view', 'View knowledge base', 'knowledge'),
    ('knowledge.manage', 'Manage knowledge base', 'knowledge'),
    ('integrations.view', 'View integrations', 'integrations'),
    ('integrations.manage', 'Manage integrations', 'integrations'),
    ('sales.view', 'View sales', 'sales'),
    ('sales.manage', 'Manage sales', 'sales'),
    ('billing.view', 'View billing', 'billing'),
    ('billing.manage', 'Manage billing', 'billing')
ON CONFLICT (name) DO NOTHING;

-- Insert default onboarding steps
INSERT INTO onboarding_steps (step_key, title, description, "order", is_required) VALUES
    ('welcome', 'Welcome & Setup', 'Get started with your account', 1, true),
    ('connect_channel', 'Connect Channels', 'Integrate your communication channels', 2, true),
    ('configure_ai_rules', 'Configure AI Rules', 'Set up your automation rules', 3, true),
    ('add_knowledge', 'Add Knowledge Base', 'Upload FAQs and responses', 4, true),
    ('review_analytics', 'Review Analytics', 'Explore your dashboard', 5, false),
    ('invite_team', 'Invite Team Members', 'Add team members to your workspace', 6, false)
ON CONFLICT (step_key) DO NOTHING;
"""

def run_migration():
    """Run the migration to create all tables."""
    print("Starting database migration...")
    
    with engine.connect() as connection:
        try:
            # Execute all SQL statements
            connection.execute(text(MIGRATION_SQL))
            connection.commit()
            print("✓ Migration completed successfully!")
            print("✓ All tables created")
            print("✓ Default permissions inserted")
            print("✓ Default onboarding steps inserted")
        except Exception as e:
            connection.rollback()
            print(f"✗ Migration failed: {e}")
            raise

if __name__ == "__main__":
    run_migration()

