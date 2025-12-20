# Database Schema Contract - FROZEN

## 🚫 SCHEMA FREEZE DECLARATION

**Effective Date:** Current Date  
**Status:** ✅ **FROZEN**  
**Version:** 1.0

---

## Frozen Tables (10)

| Table Name | Purpose | Status |
|------------|---------|--------|
| `conversations` | User-bot interactions | ✅ FROZEN |
| `users` | Authentication & access control | ✅ FROZEN |
| `businesses` | Multi-tenant workspaces | ✅ FROZEN |
| `channel_integrations` | Platform connections | ✅ FROZEN |
| `messages` | Individual message tracking | ✅ FROZEN |
| `leads` | Lead capture & tracking | ✅ FROZEN |
| `knowledge_entries` | FAQ/knowledge base | ✅ FROZEN |
| `conversation_memory` | User context tracking | ✅ FROZEN |
| `analytics_events` | System event tracking | ✅ FROZEN |
| `ad_assets` | Ad & video assets | ✅ FROZEN |

---

## Frozen Fields Per Table

### `conversations`
- `id` (Integer, PK)
- `user_id` (String, indexed)
- `channel` (String, indexed)
- `user_message` (Text)
- `bot_reply` (Text)
- `intent` (String, indexed)
- `created_at` (DateTime, indexed)

### `users`
- `id` (Integer, PK)
- `email` (String, unique, indexed)
- `hashed_password` (String)
- `full_name` (String, nullable)
- `role` (String, default="agent")
- `is_active` (Boolean, default=True)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### `businesses`
- `id` (Integer, PK)
- `name` (String, indexed)
- `owner_id` (Integer, FK to users.id)
- `settings` (Text, JSON)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### `channel_integrations`
- `id` (Integer, PK)
- `business_id` (Integer, FK to businesses.id)
- `channel` (String, indexed)
- `channel_name` (String, nullable)
- `credentials` (Text, encrypted JSON)
- `is_active` (Boolean, default=True)
- `webhook_url` (String, nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### `messages`
- `id` (Integer, PK)
- `conversation_id` (Integer, FK to conversations.id, nullable)
- `user_id` (String, indexed)
- `channel` (String, indexed)
- `message_text` (Text)
- `is_from_user` (Boolean)
- `intent` (String, nullable, indexed)
- `created_at` (DateTime, indexed)

### `leads`
- `id` (Integer, PK)
- `business_id` (Integer, FK to businesses.id)
- `user_id` (String, indexed)
- `channel` (String, indexed)
- `name` (String, nullable)
- `email` (String, nullable, indexed)
- `phone` (String, nullable)
- `status` (String, default="new", indexed)
- `source_intent` (String, nullable)
- `extra_data` (Text, JSON)
- `created_at` (DateTime, indexed)
- `updated_at` (DateTime)

### `knowledge_entries`
- `id` (Integer, PK)
- `business_id` (Integer, FK to businesses.id)
- `question` (Text)
- `answer` (Text)
- `keywords` (Text, JSON array)
- `intent` (String, nullable, indexed)
- `is_active` (Boolean, default=True)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### `conversation_memory`
- `id` (Integer, PK)
- `user_id` (String, indexed)
- `channel` (String, indexed)
- `last_intent` (String, nullable)
- `message_count` (Integer, default=0)
- `context_data` (Text, JSON)
- `updated_at` (DateTime)

### `analytics_events`
- `id` (Integer, PK)
- `business_id` (Integer, FK to businesses.id, nullable)
- `event_type` (String, indexed)
- `event_data` (Text, JSON)
- `channel` (String, nullable, indexed)
- `user_id` (String, nullable, indexed)
- `created_at` (DateTime, indexed)

### `ad_assets`
- `id` (Integer, PK)
- `business_id` (Integer, FK to businesses.id)
- `asset_type` (String)
- `title` (String)
- `content` (Text, nullable)
- `platform` (String, nullable)
- `status` (String, default="draft")
- `extra_data` (Text, JSON)
- `created_at` (DateTime)
- `updated_at` (DateTime)

---

## Change Policy

### ❌ PROHIBITED (Breaking Changes)
- Delete any column
- Rename any column
- Change column data type
- Remove any index
- Change any foreign key relationship
- Make any NOT NULL column nullable (without migration)

### ✅ ALLOWED (Non-Breaking Changes)
- Add new nullable columns
- Add new tables
- Add new indexes
- Add new foreign keys (to new tables)
- Add new constraints (that don't affect existing data)

---

## Forward Compatibility Status

### ✅ Payments Integration - READY
- `businesses` table supports subscription linking
- `leads` table supports conversion tracking
- Future: Add `subscriptions` and `payments` tables

### ✅ Analytics Integration - READY
- `analytics_events` table supports flexible event tracking
- `conversations` and `messages` support conversation analytics
- Future: Add `event_category` and `event_value` fields

### ✅ LLM Integration - READY
- `conversations.bot_reply` supports LLM responses
- `conversation_memory.context_data` supports conversation history
- `knowledge_entries` supports vector embeddings (future)
- Future: Add `model_name` and `tokens_used` fields

---

## Security Notes

### 🔴 High Priority
- `channel_integrations.credentials` - **MUST** be encrypted at application level
- `users.hashed_password` - **MUST** use bcrypt/argon2 (verified in auth service)

### ✅ Verified
- Password hashing implemented in `app/services/auth.py`
- Credentials field exists (encryption required in application code)

---

## Naming Conventions (Frozen)

### Table Names
- Plural, lowercase, snake_case
- Examples: `conversations`, `users`, `businesses`

### Column Names
- lowercase, snake_case, descriptive
- Foreign keys: `{table}_id` (e.g., `user_id`, `business_id`)
- Timestamps: `created_at`, `updated_at`
- Booleans: `is_{condition}` (e.g., `is_active`, `is_from_user`)
- JSON fields: `{purpose}_data` (e.g., `context_data`, `event_data`)

---

## Migration Strategy

### Current Phase: SQLite
- No length limits on String columns
- Text type for JSON fields
- Flexible schema

### Future Phase: PostgreSQL
- Add String length limits (e.g., `String(255)`)
- Convert Text JSON to JSON/JSONB type
- Add explicit foreign key constraints

**Note:** SQLAlchemy ORM abstraction allows migration without code changes.

---

## Summary

✅ **Schema Quality:** Excellent  
✅ **Naming:** Consistent and clear  
✅ **Forward Compatibility:** Ready for payments, analytics, LLMs  
✅ **Security:** Proper field design (encryption required in application)  
✅ **Status:** **FROZEN** - Ready for stabilization phase

---

**Contract Version:** 1.0  
**Last Updated:** Current Date  
**Next Review:** Post-stabilization phase


