"""Script to create the first admin user.

Run this script to create an admin user for the dashboard.

Usage:
    python create_admin_user.py
"""
import sys
from app.database import get_db_context
from app.services.auth import create_user, get_user_by_email

def main():
    email = input("Enter admin email: ").strip()
    if not email:
        print("Email is required")
        sys.exit(1)

    password = input("Enter admin password: ").strip()
    if not password or len(password) < 6:
        print("Password must be at least 6 characters")
        sys.exit(1)

    full_name = input("Enter full name (optional): ").strip() or None

    try:
        with get_db_context() as db:
            # Check if user already exists
            existing = get_user_by_email(db, email)
            if existing:
                print(f"❌ User with email {email} already exists")
                sys.exit(1)

            # Create user
            user = create_user(
                db,
                email=email,
                password=password,
                full_name=full_name,
                role="admin"
            )
            print(f"✅ Admin user created successfully!")
            print(f"   Email: {user.email}")
            print(f"   Role: {user.role}")
            print(f"   ID: {user.id}")
            print(f"\nYou can now login at http://localhost:3000/login")
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



