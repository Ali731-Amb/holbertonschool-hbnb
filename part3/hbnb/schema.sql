-- Supprime les tables dans le bon ordre (enfants avant parents)
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- =====================
-- TABLE : users
-- =====================
CREATE TABLE users (
    id            CHAR(36)     PRIMARY KEY,
    first_name    VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50)  NOT NULL,
    email         VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    is_admin      BOOLEAN      DEFAULT FALSE,
    pet           VARCHAR(20)
);

-- =====================
-- TABLE : places
-- =====================
CREATE TABLE places (
    id          CHAR(36)       PRIMARY KEY,
    title       VARCHAR(255),
    description TEXT,
    price       DECIMAL(10, 2),
    latitude    FLOAT,
    longitude   FLOAT,
    owner_id    CHAR(36)       NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- =====================
-- TABLE : reviews
-- =====================
CREATE TABLE reviews (
    id       CHAR(36) PRIMARY KEY,
    text     TEXT,
    rating   INT CHECK (rating >= 1 AND rating <= 5),
    user_id  CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id)
);

-- =====================
-- TABLE : amenities
-- =====================
CREATE TABLE amenities (
    id   CHAR(36)     PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- =====================
-- TABLE : place_amenity
-- =====================
CREATE TABLE place_amenity (
    place_id   CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id)   REFERENCES places(id)    ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);