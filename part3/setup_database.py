#!/usr/bin/env python3
"""
HBnB - Database Setup Script
"""

import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import DevelopmentConfig
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


def main():

    print("\n" + "=" * 60)
    print("HBnB Database Setup")
    print("=" * 60)

    app = create_app("development")

    with app.app_context():
        try:
            # Step 1: Drop & Create tables
            print("\nDropping existing tables...")
            db.drop_all()

            print("Creating fresh tables...")
            db.create_all()

            print("✅ Tables ready!")

            # Step 2: Create Users
            print("\n📝 Creating users...")

            admin = User(
                id=str(uuid.uuid4()),
                first_name='Raghad',
                last_name='Almalki',
                email='raghad@hbnb.com',
                is_admin=True
            )
            admin.hash_password('admin123')
            db.session.add(admin)

            jana = User(
                id=str(uuid.uuid4()),
                first_name='Jana',
                last_name='Bakri',
                email='jana@hbnb.com',
                is_admin=False
            )
            jana.hash_password('jana123')
            db.session.add(jana)

            rama = User(
                id=str(uuid.uuid4()),
                first_name='Rama',
                last_name='Alshahri',
                email='rama@hbnb.com',
                is_admin=False
            )
            rama.hash_password('rama123')
            db.session.add(rama)

            db.session.commit()
            print(f"✅ Created {User.query.count()} users")

            # Step 3: Amenities
            print("\n📝 Creating amenities...")

            amenities_names = ['WiFi', 'Pool', 'Parking', 'Breakfast', 'Gym', 'AC']
            amenities = {}

            for name in amenities_names:
                a = Amenity(id=str(uuid.uuid4()), name=name)
                db.session.add(a)
                amenities[name] = a

            db.session.commit()
            print(f"✅ Created {Amenity.query.count()} amenities")

            # Step 4: Places
            print("\n📝 Creating places...")

            place1 = Place(
                id=str(uuid.uuid4()),
                title='Luxury Resort Riyadh',
                description='A luxury resort in the heart of Riyadh',
                price=100.0,
                latitude=24.7136,
                longitude=46.6753,
                owner_id=admin.id
            )

            place1.amenities.append(amenities['WiFi'])
            place1.amenities.append(amenities['Pool'])
            place1.amenities.append(amenities['Parking'])
            place1.amenities.append(amenities['Breakfast'])

            db.session.add(place1)

            db.session.commit()
            print(f"✅ Created {Place.query.count()} places")

            # Step 5: Reviews
            print("\n📝 Creating reviews...")

            reviews_data = [
                (place1.id, jana.id, 5, 'Amazing place!'),
                (place1.id, rama.id, 4, 'Great experience!'),
            ]

            for place_id, user_id, rating, text in reviews_data:
                review = Review(
                    id=str(uuid.uuid4()),
                    place_id=place_id,
                    user_id=user_id,
                    rating=rating,
                    text=text
                )
                db.session.add(review)

            db.session.commit()
            print(f"✅ Created {Review.query.count()} reviews")

            print("\n🎉 DONE SUCCESSFULLY!")

            return 0

        except Exception as e:
            print(f"\n❌ Error: {e}")
            db.session.rollback()
            return 1


if __name__ == '__main__':
    exit(main())
