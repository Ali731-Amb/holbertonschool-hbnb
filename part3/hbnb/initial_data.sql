-- =====================
-- Utilisateur Admin
-- =====================
DELETE FROM Place_Amenity;
DELETE FROM Review;
DELETE FROM Place;
DELETE FROM Amenity;
DELETE FROM users;
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$TKJDoP1SU0XvHXtQX.UDGeFoDYxNcy8ibONHnA6Rm1X4OPv2EzZj6',
    TRUE
);

-- =====================
-- Amenities
-- =====================
INSERT INTO Amenity (id, name) VALUES ('467073a3-b3c0-4c1f-9831-5467a67dcea5',          'WiFi');
INSERT INTO Amenity (id, name) VALUES ('160cb549-80bc-4f3d-9184-5bd98a914c24',       'Piscine');
INSERT INTO Amenity (id, name) VALUES ('b6b08f7c-e8c0-48fd-9acf-d265d19fe09d', 'Climatisation');
