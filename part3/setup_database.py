#!/usr/bin/env python3
"""
HBnB - Database Setup Script
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import DevelopmentConfig
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

def main():
    print("\n" + "="*60)
    print("HBnB Database Setup")
    print("="*60)

    app = create_app(DevelopmentConfig)

    with app.app_context():
        try:
            # Step 1: Drop & Create tables
            print("\nDropping existing tables...")
            db.drop_all()
            print("Creating fresh tables...")
            db.create_all()
            print("Tables ready!")

            # Step 2: Create Users
            print("\nCreating users...")

            admin = User(
                first_name='Admin',
                last_name='HBnB',
                email='admin@hbnb.com',
                password='admin123',
                is_admin=True
            )
            db.session.add(admin)

            rama = User(
                first_name='rama',
                last_name='Alsheheri',
                email='ramadafer1@gmail.com',
                password='ra2004',
                is_admin=False
            )
            db.session.add(rama)

            jana = User(
                first_name='jana',
                last_name='bakri',
                email='bkeyh382@gmail.com',
                password='jana2',
                is_admin=False
            )
            db.session.add(jana)

            raghad = User(
                first_name='raghad',
                last_name='almalki',
                email='raghad2@hotmail.com',
                password='raghad2',
                is_admin=False
            )
            db.session.add(raghad)

            db.session.commit()
            print(f"Created {User.query.count()} users")

            # Step 3: Create Amenities
            print("\nCreating amenities...")

            amenities_names = ['WiFi', 'Pool', 'Parking', 'Breakfast', 'Gym', 'AC']
            amenities = {}

            for name in amenities_names:
                a = Amenity(name=name)
                db.session.add(a)
                amenities[name] = a

            db.session.commit()
            print(f"Created {Amenity.query.count()} amenities")

            # Step 4: Create Places
            print("\nCreating places...")

            place1 = Place(
                title='Luxury Resort Riyadh-Diryiah',
                description='A luxury resort in the heart of Riyadh with all modern amenities.',
                price=50.0,
                latitude=24.7136,
                longitude=46.6753,
                owner_id=admin.id
            )
            place1.amenities.append(amenities['WiFi'])
            place1.amenities.append(amenities['Pool'])
            place1.amenities.append(amenities['Parking'])
            place1.amenities.append(amenities['Breakfast'])
            db.session.add(place1)

            place2 = Place(
                title='Modern City Hotel ',
                description='A modern hotel in the city center with a great view.',
                price=100.0,
                latitude=24.7242,
                longitude=46.6385,
                owner_id=admin.id
            )
            place2.amenities.append(amenities['WiFi'])
            place2.amenities.append(amenities['Parking'])
            place2.amenities.append(amenities['Gym'])
            db.session.add(place2)

            place3 = Place(
                title='Cozy Downtown Apartment',
                description='Comfortable apartment in the city center, suitable for families.',
                price=50.0,
                latitude=24.7353,
                longitude=46.5752,
                owner_id=admin.id
            )
            place3.amenities.append(amenities['WiFi'])
            place3.amenities.append(amenities['AC'])
            db.session.add(place3)

            place4 = Place(
                title='Family Villa with Garden',
                description='Luxury family villa with a spacious garden.',
                price=10.0,
                latitude=24.6877,
                longitude=46.7219,
                owner_id=admin.id
            )
            place4.amenities.append(amenities['WiFi'])
            place4.amenities.append(amenities['Pool'])
            place4.amenities.append(amenities['Parking'])
            db.session.add(place4)

            place5 = Place(
                title='Budget Room Near Metro',
                description='An economy room close to the metro.',
                price=90.0,
                latitude=24.7500,
                longitude=46.6900,
                owner_id=admin.id
            )
            place5.amenities.append(amenities['WiFi'])
            db.session.add(place5)

            db.session.commit()
            print(f"Created {Place.query.count()} places")

            # Step 5: Create Reviews
            print("\nCreating reviews...")

            reviews_data = [
                (place1.id, rama.id,   5, 'Amazing place! Highly recommended.'),
                (place1.id, jana.id,  4, 'Great experience, clean and lovely service.'),
                (place2.id, raghad.id, 4, 'Beautiful hotel with a great location.'),
                (place3.id, jana.id,  5, 'Very comfortable apartment at a reasonable price.'),
                (place4.id, rama.id,   5, 'Luxurious villa! We loved the garden.'),
            ]

            for place_id, user_id, rating, text in reviews_data:
                review = Review(
                    place_id=place_id,
                    user_id=user_id,
                    rating=rating,
                    text=text
                )
                db.session.add(review)

            db.session.commit()
            print(f"Created {Review.query.count()} reviews")

            # Summary
            print("\n" + "="*60)
            print("Database setup completed successfully!")
            print("="*60)
            print("\nLogin Credentials:")
            print("-" * 60)
            print("  admin@hbnb.com           | admin123  | (Admin)")
            print("  ramadafer1@gmail.com     | ra2004      | (rama)")
            print("  bkeyh382@gmail.com       | jana2      | (jana)")
            print("  raghad2@hotmail.com      | raghad2      | (raghad)")
            print("-" * 60)
            print(f"\nUsers:     {User.query.count()}")
            print(f"Places:    {Place.query.count()}")
            print(f"Reviews:   {Review.query.count()}")
            print(f"Amenities: {Amenity.query.count()}")
            print("\n" + "="*60 + "\n")

            return 0

        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return 1

if __name__ == '__main__':
    exit(main())
