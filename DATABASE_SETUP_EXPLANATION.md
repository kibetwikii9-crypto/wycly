# SQLite Database Setup Explanation

## ✅ Created `database.py`

### File: `app/database.py`

This module provides the foundation for database operations using SQLAlchemy.

---

## 📋 Parts Explanation

### 1. **Engine Creation**

```python
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=False,
)
```

**What it does:**
- Creates the SQLAlchemy engine (database connection pool)
- Uses `settings.database_url` from config (default: `sqlite:///./curie.db`)
- `check_same_thread=False`: Allows SQLite to work with FastAPI's async/multi-threaded requests
- `echo=False`: Set to `True` to log all SQL queries (useful for debugging)

**Why it matters:**
- Engine manages database connections efficiently
- Connection pooling improves performance
- Can be swapped to PostgreSQL later by changing `database_url`

---

### 2. **Session Factory**

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
```

**What it does:**
- Creates a factory for database sessions
- `autocommit=False`: We commit explicitly (better control)
- `autoflush=False`: We flush explicitly (better control)
- `bind=engine`: Connects to the engine we created

**Why it matters:**
- Sessions are the interface to the database
- Each request gets its own session
- Explicit control over commits/flushes prevents data issues

---

### 3. **Base Class**

```python
Base = declarative_base()
```

**What it does:**
- Creates the base class for all database models
- All models will inherit from this: `class User(Base): ...`
- Provides ORM functionality (Object-Relational Mapping)

**Why it matters:**
- All models share the same base
- Enables `Base.metadata.create_all()` to create all tables
- Provides consistent model structure

**Example usage:**
```python
from app.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

---

### 4. **FastAPI Dependency: `get_db()`**

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**What it does:**
- Provides a database session for FastAPI routes
- Automatically creates session at request start
- Automatically closes session at request end
- Can be used as a FastAPI dependency

**Why it matters:**
- Ensures sessions are properly closed (prevents connection leaks)
- Clean integration with FastAPI's dependency injection
- No manual session management needed

**Usage in routes:**
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

---

### 5. **Context Manager: `get_db_context()`**

```python
@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

**What it does:**
- Provides a database session for use outside FastAPI
- Can be used with Python's `with` statement
- Automatically commits on success
- Automatically rolls back on error

**Why it matters:**
- Useful for background tasks, scripts, or services
- Ensures transactions are properly handled
- Prevents data corruption on errors

**Usage:**
```python
from app.database import get_db_context

with get_db_context() as db:
    user = db.query(User).first()
    user.name = "New Name"
    # Automatically commits on success
```

---

### 6. **Database Initialization: `init_db()`**

```python
def init_db() -> None:
    Base.metadata.create_all(bind=engine)
```

**What it does:**
- Creates all database tables defined in models
- Scans all models that inherit from `Base`
- Creates tables if they don't exist

**Why it matters:**
- Simple way to set up database schema
- Useful for development and testing
- **Note:** For production, use Alembic migrations instead

**Usage:**
```python
from app.database import init_db

# On application startup
init_db()
```

---

## 🔧 Configuration

### Updated `config.py`:

```python
database_url: str = "sqlite:///./curie.db"
```

**What it does:**
- Sets the database connection string
- Default: SQLite file in project root (`./curie.db`)
- Can be overridden via environment variable: `DATABASE_URL`

**SQLite Connection String Format:**
- `sqlite:///./curie.db` - Relative path (project root)
- `sqlite:////absolute/path/to/curie.db` - Absolute path
- `sqlite:///:memory:` - In-memory database (testing)

**Future PostgreSQL:**
- `postgresql://user:password@localhost/dbname`
- Just change `database_url` - no code changes needed!

---

## 📦 Dependencies

### Added to `requirements.txt`:

```
sqlalchemy==2.0.35
```

**SQLAlchemy 2.0:**
- Modern API with better type hints
- Improved performance
- Better async support
- Backward compatible with 1.4

---

## 🎯 Usage Examples

### Example 1: Using in FastAPI Route

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

---

### Example 2: Creating a Model

```python
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

### Example 3: Using Context Manager

```python
from app.database import get_db_context
from app.models import User

def create_user(name: str, email: str):
    with get_db_context() as db:
        user = User(name=name, email=email)
        db.add(user)
        # Automatically commits on success
```

---

### Example 4: Initializing Database

```python
# In app/main.py
from app.database import init_db

@app.on_event("startup")
async def startup_event():
    init_db()  # Create all tables
```

---

## 🔄 Database Lifecycle

### 1. **Application Startup:**
```
1. Load settings (database_url)
2. Create engine
3. Create session factory
4. Initialize database (create tables)
```

### 2. **Request Handling:**
```
1. FastAPI calls get_db() dependency
2. Session created
3. Route uses session
4. Session automatically closed
```

### 3. **Transaction Flow:**
```
1. Session created
2. Queries executed
3. Changes made
4. db.commit() or db.rollback()
5. Session closed
```

---

## ✅ Benefits

1. **Simple Setup:**
   - ✅ SQLite file database (no server needed)
   - ✅ Easy to set up and test
   - ✅ Perfect for development

2. **Production Ready:**
   - ✅ Can swap to PostgreSQL easily
   - ✅ Just change `database_url`
   - ✅ No code changes needed

3. **Clean Architecture:**
   - ✅ Separation of concerns
   - ✅ Dependency injection
   - ✅ Proper session management

4. **Type Safety:**
   - ✅ SQLAlchemy 2.0 with type hints
   - ✅ Better IDE support
   - ✅ Fewer runtime errors

---

## 🚀 Next Steps

1. **Create Models:**
   - Define database models (User, Message, etc.)
   - Inherit from `Base`
   - Add columns and relationships

2. **Initialize Database:**
   - Call `init_db()` on startup
   - Or use Alembic for migrations

3. **Use in Routes:**
   - Add `db: Session = Depends(get_db)` to routes
   - Query and modify data

4. **Future: Add Migrations:**
   - Set up Alembic for schema versioning
   - Track database changes
   - Production-ready migrations

---

## 🎯 Summary

**`database.py` provides:**
- ✅ SQLAlchemy engine and session factory
- ✅ Base class for models
- ✅ FastAPI dependency (`get_db()`)
- ✅ Context manager (`get_db_context()`)
- ✅ Database initialization (`init_db()`)

**Key Features:**
- Simple SQLite setup
- Easy to upgrade to PostgreSQL
- Clean session management
- Type-safe with SQLAlchemy 2.0

The database setup is ready for Phase 3.1! You can now create models and start storing data.



