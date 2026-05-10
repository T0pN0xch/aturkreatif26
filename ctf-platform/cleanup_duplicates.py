#!/usr/bin/env python
"""
Remove duplicate challenges from the database.
Keeps the first instance of each challenge (by title).
"""

from app import create_app
from models import db, Challenge

def remove_duplicates():
    app = create_app()
    with app.app_context():
        print("🧹 Cleaning up duplicate challenges...\n")
        
        # Get all challenges
        all_challenges = Challenge.query.all()
        seen_titles = {}
        duplicates_to_delete = []
        
        # Find duplicates
        for challenge in all_challenges:
            if challenge.title in seen_titles:
                print(f"  ❌ Duplicate found: '{challenge.title}' (ID: {challenge.id})")
                duplicates_to_delete.append(challenge)
            else:
                seen_titles[challenge.title] = challenge.id
                print(f"  ✓ Keeping: '{challenge.title}' (ID: {challenge.id})")
        
        # Delete duplicates
        if duplicates_to_delete:
            print(f"\n🗑️  Deleting {len(duplicates_to_delete)} duplicate(s)...")
            for challenge in duplicates_to_delete:
                db.session.delete(challenge)
            db.session.commit()
            print(f"✅ Deleted {len(duplicates_to_delete)} duplicate challenges!")
        else:
            print("\n✅ No duplicates found!")
        
        # Show final count
        total = Challenge.query.count()
        print(f"\n📊 Final challenge count: {total}")

if __name__ == '__main__':
    remove_duplicates()
