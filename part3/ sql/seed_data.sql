-- Seed data for HBnB database

USE hbnb_db;

-- =====================================================
-- Insert admin account (password: Admin@123)
-- =====================================================
INSERT INTO accounts (user_id, given_name, family_name, email_address, password, is_administrator)
VALUES (
    'admin-001-1111-4444-8888-123456789012',
    'System',
    'Administrator',
    'admin@hbnb.com',
    '$2b$12$LQv7c1t3kYqZwKqZwKqZwKuZwKqZwKqZwKqZwKqZwKqZwKqZwKqZw', -- hashed 'Admin@123'
    TRUE
);

-- =====================================================
-- Insert sample users
-- =====================================================
INSERT INTO accounts (user_id, given_name, family_name, email_address, password, is_administrator)
VALUES
    ('user-001-2222-5555-9999-234567890123', 'John', 'Smith', 'john.smith@email.com', '$2b$12$LQv7c1t3kYqZwKqZwKqZwKuZwKqZwKqZwKqZwKqZwKqZwKqZwKqZw', FALSE),
    ('user-002-3333-6666-0000-345678901234', 'Emma', 'Johnson', 'emma.j@email.com', '$2b$12$LQv7c1t3kYqZwKqZwKqZwKuZwKqZwKqZwKqZwKqZwKqZwKqZwKqZw', FALSE),
    ('user-003-4444-7777-1111-456789012345', 'Michael', 'Brown', 'michael.b@email.com', '$2b$12$LQv7c1t3kYqZwKqZwKqZwKuZwKqZwKqZwKqZwKqZwKqZwKqZwKqZw', FALSE);

-- =====================================================
-- Insert facilities (amenities)
-- =====================================================
INSERT INTO facilities (facility_id, facility_name, facility_description)
VALUES
    ('fac-001-5555-8888-2222-567890123456', 'WiFi', 'High-speed wireless internet throughout the property'),
    ('fac-002-6666-9999-3333-678901234567', 'Parking', 'Free on-site parking available'),
    ('fac-003-7777-0000-4444-789012345678', 'Pool', 'Outdoor swimming pool (seasonal)'),
    ('fac-004-8888-1111-5555-890123456789', 'Air Conditioning', 'Central air conditioning system'),
    ('fac-005-9999-2222-6666-901234567890', 'Kitchen', 'Fully equipped kitchen with appliances'),
    ('fac-006-0000-3333-7777-012345678901', 'Pet Friendly', 'Pets are welcome (fees may apply)'),
    ('fac-007-1111-4444-8888-123456789012', 'Gym', 'Fitness center with modern equipment');

-- =====================================================
-- Insert properties (places)
-- =====================================================
INSERT INTO properties (property_id, property_title, property_description, nightly_rate, location_latitude, location_longitude, owner_id)
VALUES
    ('prop-001-2222-5555-8888-234567890123', 
     'Cozy Beachfront Apartment', 
     'Beautiful apartment with stunning ocean views. Walking distance to restaurants and shops.', 
     149.99, 25.7617, -80.1918, 
     'user-001-2222-5555-9999-234567890123'),
    
    ('prop-002-3333-6666-9999-345678901234', 
     'Mountain View Cabin', 
     'Rustic cabin in the woods with spectacular mountain views. Perfect for hiking enthusiasts.', 
     199.50, 39.5501, -105.7821, 
     'user-002-3333-6666-0000-345678901234'),
    
    ('prop-003-4444-7777-0000-456789012345', 
     'Downtown Loft', 
     'Modern loft in the heart of the city. Close to nightlife, restaurants, and public transport.', 
     129.99, 34.0522, -118.2437, 
     'user-003-4444-7777-1111-456789012345');

-- =====================================================
-- Link properties with facilities
-- =====================================================
INSERT INTO property_facility (property_id, facility_id)
VALUES
    -- Cozy Beachfront Apartment amenities
    ('prop-001-2222-5555-8888-234567890123', 'fac-001-5555-8888-2222-567890123456'), -- WiFi
    ('prop-001-2222-5555-8888-234567890123', 'fac-002-6666-9999-3333-678901234567'), -- Parking
    ('prop-001-2222-5555-8888-234567890123', 'fac-004-8888-1111-5555-890123456789'), -- AC
    
    -- Mountain View Cabin amenities
    ('prop-002-3333-6666-9999-345678901234', 'fac-001-5555-8888-2222-567890123456'), -- WiFi
    ('prop-002-3333-6666-9999-345678901234', 'fac-005-9999-2222-6666-901234567890'), -- Kitchen
    ('prop-002-3333-6666-9999-345678901234', 'fac-006-0000-3333-7777-012345678901'), -- Pet Friendly
    
    -- Downtown Loft amenities
    ('prop-003-4444-7777-0000-456789012345', 'fac-001-5555-8888-2222-567890123456'), -- WiFi
    ('prop-003-4444-7777-0000-456789012345', 'fac-004-8888-1111-5555-890123456789'), -- AC
    ('prop-003-4444-7777-0000-456789012345', 'fac-007-1111-4444-8888-123456789012'); -- Gym

-- =====================================================
-- Insert feedbacks (reviews)
-- =====================================================
INSERT INTO feedbacks (feedback_id, comment, score, author_id, property_id)
VALUES
    ('rev-001-5555-8888-1111-678901234567',
     'Amazing place! The view was breathtaking and the host was very responsive.',
     5, 'user-002-3333-6666-0000-345678901234',
     'prop-001-2222-5555-8888-234567890123'),
    
    ('rev-002-6666-9999-2222-789012345678',
     'Great location, but the apartment was a bit smaller than expected.',
     4, 'user-003-4444-7777-1111-456789012345',
     'prop-001-2222-5555-8888-234567890123'),
    
    ('rev-003-7777-0000-3333-890123456789',
     'Perfect mountain getaway! Loved the peace and quiet.',
     5, 'user-001-2222-5555-9999-234567890123',
     'prop-002-3333-6666-9999-345678901234');
