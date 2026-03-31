-- Supprime les tables si elles existent déjà (pour pouvoir relancer proprement)
DROP TABLE IF EXISTS Place_Amenity;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Place;
DROP TABLE IF EXISTS Amenity;
DROP TABLE IF EXISTS User;

-- =====================
-- TABLE : User
-- =====================
CREATE TABLE User (
    id         CHAR(36)     PRIMARY KEY,
    first_name VARCHAR(255),
    last_name  VARCHAR(255),
    email      VARCHAR(255) UNIQUE NOT NULL,
    password   VARCHAR(255) NOT NULL,
    is_admin   BOOLEAN      DEFAULT FALSE
);

-- =====================
-- TABLE : Place
-- =====================
CREATE TABLE Place (
    id          CHAR(36)       PRIMARY KEY,
    title       VARCHAR(255),
    description TEXT,
    price       DECIMAL(10, 2),
    latitude    FLOAT,
    longitude   FLOAT,
    owner_id    CHAR(36)       NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id)
);

-- =====================
-- TABLE : Review
-- =====================
CREATE TABLE Review (
    id       CHAR(36) PRIMARY KEY,
    text     TEXT,
    rating   INT CHECK (rating >= 1 AND rating <= 5),
    user_id  CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id)  REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    UNIQUE (user_id, place_id)   -- un seul avis par utilisateur par lieu
);

-- =====================
-- TABLE : Amenity
-- =====================
CREATE TABLE Amenity (
    id   CHAR(36)     PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- =====================
-- TABLE : Place_Amenity (relation Many-to-Many)
-- =====================
CREATE TABLE Place_Amenity (
    place_id   CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),          -- clé primaire composite
    FOREIGN KEY (place_id)   REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);