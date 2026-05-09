#!/usr/bin/env python
"""
Initialize the CTF platform database and create an admin user.
Run this script after installing dependencies and before starting the app.
"""

from app import create_app
from models import db, User
import secrets

def init_database():
    """Initialize the database"""
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database initialized!")

def create_admin_user():
    """Create an admin user"""
    app = create_app()
    with app.app_context():
        print("\n=== Create Admin User ===")
        username = input("Enter admin username: ").strip()
        
        if User.query.filter_by(username=username).first():
            print("✗ Username already exists!")
            return
        
        email = input("Enter admin email: ").strip()
        password = input("Enter admin password: ").strip()
        
        if not username or not email or not password:
            print("✗ All fields required!")
            return
        
        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        print(f"✓ Admin user '{username}' created successfully!")
        print(f"  You can now login at http://localhost:5000/login")

def main():
    print("🚩 CTF Platform - Database Initialization\n")
    
    init_database()
    
    create_admin = input("\nCreate admin user? (y/n): ").lower() == 'y'
    if create_admin:
        create_admin_user()
    
    print("\n✓ Setup complete! Run 'python app.py' to start the server.")

if __name__ == '__main__':
    main()
