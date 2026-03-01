USE hbnb_db;

-- Insert admin user (password: admin123)
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'Admin',
    'User',
    'admin@hbnb.com',
    '$2b$12$LQv7c1t3kYqZwKqZwKqZwKuZwKqZwKqZwKqZwKqZwKqZwKqZwKqZw',
    TRUE
);

-- Insert amenities
INSERT INTO amenities (id, name, description)
VALUES 
    ('22222222-2222-2222-2222-222222222222', 'WiFi', 'High-speed wireless internet'),
    ('33333333-3333-3333-3333-333333333333', 'Parking', 'Free parking on premises'),
    ('44444444-4444-4444-4444-444444444444', 'Pool', 'Outdoor swimming pool'),
    ('55555555-5555-5555-5555-555555555555', 'Air Conditioning', 'Central air conditioning');
