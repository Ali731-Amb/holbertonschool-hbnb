-- =====================
-- Utilisateur Admin
-- =====================
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$nrTz9KQhFXIT9iGi2osIt.YTVbNHg0rCpWxU.Sxq.eAnbrMcwzzP6',   -- remplace par le hash généré à l'étape 2
    TRUE
);

-- =====================
-- Amenities
-- =====================
INSERT INTO Amenity (id, name) VALUES ('467073a3-b3c0-4c1f-9831-5467a67dcea5',          'WiFi');
INSERT INTO Amenity (id, name) VALUES ('160cb549-80bc-4f3d-9184-5bd98a914c24',       'Piscine');
INSERT INTO Amenity (id, name) VALUES ('Ub6b08f7c-e8c0-48fd-9acf-d265d19fe09d', 'Climatisation');