# HBnB Evolution — Full Stack Project

<img width="960" height="1106" alt="Gemini_Generated_Image_fdffewfdffewfdff" src="https://github.com/user-attachments/assets/6d51b852-722e-4f4c-99af-d566103cadf0" />


> A full-stack AirBnB-inspired web application built at Holberton School.  
> **Author:** Alison Amblard | [GitHub: Ali731-Amb](https://github.com/Ali731-Amb)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Part 1 — UML & Design](#part-1--uml--design)
4. [Part 2 — Backend API (In-Memory)](#part-2--backend-api-in-memory)
5. [Part 3 — Database & Authentication](#part-3--database--authentication)
6. [Part 4 — Web Client (Frontend)](#part-4--web-client-frontend)
7. [Getting Started](#getting-started)
8. [API Reference](#api-reference)
9. [Test Data](#test-data)
10. [Author](#author)

---

## Project Overview

HBnB Evolution is a full-stack web application built over 4 parts as part of the Holberton School curriculum. It allows users to browse rental places, view details, and submit reviews — with full authentication via JWT tokens.

The project is structured as follows:

| Part | Description                              | Stack                          |
|------|------------------------------------------|--------------------------------|
| 1    | UML diagrams & system design             | Draw.io / Mermaid              |
| 2    | RESTful API with in-memory storage       | Python, Flask, Flask-RESTX     |
| 3    | Persistent storage + JWT authentication  | SQLAlchemy, SQLite, Flask-JWT  |
| 4    | Web client connecting to the API         | HTML5, CSS3, Vanilla JS        |

---

## Architecture

```
holbertonschool-hbnb/
├── part1/          # UML diagrams and design documentation
├── part2/          # Flask API with in-memory storage
├── part3/          # Flask API with SQLAlchemy + JWT
└── part4/
    ├── frontend/   # HTML/CSS/JS web client
    └── backend/    # Flask API (production version)
```

### Global Architecture

```
[Browser - Frontend]
        |
        | HTTP / Fetch API (JSON)
        |
[Flask API - Backend :5000]
        |
        | SQLAlchemy ORM
        |
[SQLite Database - hbnb_dev.db]
```

### Design Patterns Used
- **Facade Pattern** — `app/services/facade.py` acts as a single entry point for all business logic
- **Repository Pattern** — `app/persistence/` abstracts all database operations
- **Factory Pattern** — `create_app()` in `app/__init__.py`

---

## Part 1 — UML & Design

### Objectives
- Design the full system architecture before writing any code
- Create UML diagrams for all entities and their relationships
- Document all API endpoints and business rules

### Deliverables

#### Class Diagram
The application has 4 main entities:

```
BaseModel (abstract)
    ├── User
    │     ├── id (UUID)
    │     ├── first_name
    │     ├── last_name
    │     ├── email (unique)
    │     ├── password_hash
    │     └── is_admin (bool)
    ├── Place
    │     ├── id (UUID)
    │     ├── title
    │     ├── description
    │     ├── price
    │     ├── latitude / longitude
    │     └── owner_id → User
    ├── Review
    │     ├── id (UUID)
    │     ├── text
    │     ├── rating (1-5)
    │     ├── user_id → User
    │     └── place_id → Place
    └── Amenity
          ├── id (UUID)
          └── name
```

#### Relationships
- User `1` → `*` Place (owner)
- User `1` → `*` Review (author)
- Place `1` → `*` Review
- Place `*` ↔ `*` Amenity (via `place_amenity` table)

#### Business Rules
- A user cannot review their own place
- A user can only review a place once
- Only the owner can update/delete their place
- Only the author can update/delete their review
- Admin users can manage all resources

---

## Part 2 — Backend API (In-Memory)

### Objectives
- Implement the RESTful API using Flask and Flask-RESTX
- Use in-memory storage (Python dictionaries) for rapid prototyping
- Apply the Facade and Repository patterns

### Stack
- Python 3.10+
- Flask
- Flask-RESTX (Swagger auto-documentation)
- UUID for entity IDs

### Endpoints Implemented

| Method | Endpoint                        | Description                    | Auth |
|--------|---------------------------------|--------------------------------|------|
| POST   | `/api/v1/users/`                | Create a user                  | No   |
| GET    | `/api/v1/users/`                | List all users                 | No   |
| GET    | `/api/v1/users/<id>`            | Get user by ID                 | No   |
| PUT    | `/api/v1/users/<id>`            | Update user                    | No   |
| POST   | `/api/v1/places/`               | Create a place                 | No   |
| GET    | `/api/v1/places/`               | List all places                | No   |
| GET    | `/api/v1/places/<id>`           | Get place details              | No   |
| PUT    | `/api/v1/places/<id>`           | Update place                   | No   |
| POST   | `/api/v1/reviews/`              | Create a review                | No   |
| GET    | `/api/v1/reviews/`              | List all reviews               | No   |
| GET    | `/api/v1/reviews/<id>`          | Get review by ID               | No   |
| PUT    | `/api/v1/reviews/<id>`          | Update review                  | No   |
| DELETE | `/api/v1/reviews/<id>`          | Delete review                  | No   |
| POST   | `/api/v1/amenities/`            | Create an amenity              | No   |
| GET    | `/api/v1/amenities/`            | List all amenities             | No   |
| GET    | `/api/v1/amenities/<id>`        | Get amenity by ID              | No   |
| PUT    | `/api/v1/amenities/<id>`        | Update amenity                 | No   |

### Project Structure (Part 2)
```
part2/
└── hbnb/
    ├── app/
    │   ├── api/v1/
    │   │   ├── users.py
    │   │   ├── places.py
    │   │   ├── reviews.py
    │   │   └── amenities.py
    │   ├── models/
    │   │   ├── base_model.py
    │   │   ├── user.py
    │   │   ├── place.py
    │   │   ├── review.py
    │   │   └── amenity.py
    │   ├── persistence/
    │   │   └── repository.py   # In-memory storage
    │   ├── services/
    │   │   └── facade.py
    │   └── __init__.py
    ├── config.py
    ├── requirements.txt
    └── run.py
```

### Running Part 2
```bash
cd part2/hbnb
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 run.py
```

---

## Part 3 — Database & Authentication

### Objectives
- Replace in-memory storage with a persistent SQLite database via SQLAlchemy
- Add JWT-based authentication
- Implement role-based access control (admin vs regular user)
- Add password hashing with bcrypt

### New Stack
- SQLAlchemy (ORM)
- Flask-JWT-Extended (JWT tokens)
- Flask-Bcrypt (password hashing)
- SQLite (database)

### Database Schema

```sql
users          → id, first_name, last_name, email, password_hash, is_admin, pet
places         → id, title, description, price, latitude, longitude, owner_id
reviews        → id, text, rating, user_id, place_id  [UNIQUE(user_id, place_id)]
amenities      → id, name
place_amenity  → place_id, amenity_id  [junction table]
```

### Authentication Flow

```
POST /api/v1/auth/login  {email, password}
        ↓
Verify password with bcrypt
        ↓
Generate JWT token with claims: {sub: user_id, is_admin: bool}
        ↓
Return {access_token: "eyJ..."}
        ↓
Client sends: Authorization: Bearer <token>
        ↓
@jwt_required() decorators protect routes
```

### New/Updated Endpoints

| Method | Endpoint                        | Description                    | Auth        |
|--------|---------------------------------|--------------------------------|-------------|
| POST   | `/api/v1/auth/login`            | Login, get JWT token           | No          |
| GET    | `/api/v1/auth/protected`        | Test protected route           | JWT         |
| POST   | `/api/v1/users/`                | Create user                    | JWT         |
| PUT    | `/api/v1/users/<id>`            | Update own profile             | JWT (owner) |
| POST   | `/api/v1/users/users/`          | Admin: create any user         | JWT (admin) |
| PUT    | `/api/v1/users/users/<id>`      | Admin: update any user         | JWT (admin) |
| POST   | `/api/v1/places/`               | Create a place                 | JWT         |
| PUT    | `/api/v1/places/<id>`           | Update own place               | JWT (owner) |
| POST   | `/api/v1/reviews/`              | Create a review                | JWT         |
| PUT    | `/api/v1/reviews/<id>`          | Update own review              | JWT (owner) |
| DELETE | `/api/v1/reviews/<id>`          | Delete own review              | JWT (owner) |

### Validation Rules

**User**
- `first_name` / `last_name`: non-empty, max 50 chars
- `email`: must contain `@`, end with `.com` or `.fr`
- `password`: min 8 chars, 1 uppercase, 1 digit

**Place**
- `title`: string, max 100 chars
- `price`: positive number
- `latitude`: between -90.0 and 90.0
- `longitude`: between -180.0 and 180.0

**Review**
- `rating`: integer between 1 and 5
- Cannot review your own place
- Cannot review the same place twice

### Running Part 3
```bash
cd part3/hbnb
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sqlite3 instance/hbnb_dev.db < schema.sql
sqlite3 instance/hbnb_dev.db < initial_data.sql
python3 run.py
```

---

## Part 4 — Web Client (Frontend)

### Objectives
- Build a web client in vanilla JS connecting to the Part 3/4 API
- Implement all 4 pages: Login, Index, Place Details, Add Review
- Manage authentication via JWT cookies
- Follow the provided HTML/CSS base files from Holberton

### Stack
- HTML5 (semantic elements)
- CSS3 (custom, no framework)
- JavaScript ES6 (vanilla, no library)
- Fetch API for all HTTP requests
- JWT stored in browser cookies

### Pages

#### `login.html` — Login Form
- Email + password form
- On success: stores JWT in cookie, redirects to `index.html`
- On failure: displays error message in the form (no alert)

#### `index.html` — Place List
- Fetches all places from `GET /api/v1/places/`
- Displays each place as a card with title, price, "View Details" button
- Client-side price filter (dropdown: 10, 50, 100, All)
- Shows/hides Login link based on auth state

#### `place.html` — Place Details
- Reads `?id=` from URL
- Fetches place from `GET /api/v1/places/<id>`
- Displays: title, host, price, description, amenities, reviews with star ratings
- Shows "Add a Review" section only if authenticated

#### `add_review.html` — Add Review
- Reads `?id=` from URL
- Redirects to `index.html` if not authenticated
- Displays "Reviewing: [place title]" dynamically
- Submits review to `POST /api/v1/reviews/`

### JavaScript Architecture (`scripts.js`)

```
DOMContentLoaded
    ├── login.html detected    → loginUser()
    ├── index.html detected    → checkAuthentication()
    │                             setupPriceFilter()
    │                             fetchPlaces(token)
    ├── place.html detected    → checkAuthentication()
    │                             fetchPlaceDetails(token, placeId)
    │                             show/hide #add-review
    └── add_review.html detected → checkAuthentication(redirect=true)
                                   fetch place title
                                   submitReview()
```

### Key Functions

| Function                | Description                                  |
|-------------------------|----------------------------------------------|
| `getCookie(name)`       | Read a cookie value by name                  |
| `getPlaceIdFromURL()`   | Extract `?id=` from current URL              |
| `checkAuthentication()` | Show/hide login link, return token or null   |
| `loginUser()`           | POST to auth/login, store token in cookie    |
| `fetchPlaces()`         | GET all places, call displayPlaces()         |
| `displayPlaces()`       | Create place cards dynamically               |
| `setupPriceFilter()`    | Inject options, filter cards by data-price   |
| `fetchPlaceDetails()`   | GET place by ID, call displayPlaceDetails()  |
| `displayPlaceDetails()` | Populate title, info, reviews sections       |
| `submitReview()`        | POST review with token, text, rating         |

### CSS Design

Palette inspired by the provided mockups:

| Element         | Color             |
|-----------------|-------------------|
| Header          | `#FF5A00` (orange)|
| Footer          | `#FF5A00` (orange)|
| Buttons         | `#FF5A00` (orange)|
| Background      | `#f4f4f4` (gray)  |
| Cards           | `#ffffff` (white) |
| Card border     | `1px solid #ddd`  |
| Card radius     | `10px`            |
| Card margin     | `20px`            |
| Card padding    | `10px`            |

### Project Structure (Part 4)

```
part4/
├── frontend/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── scripts.js
│   ├── assets/
│   │   └── logo.png
│   ├── index.html
│   ├── login.html
│   ├── place.html
│   └── add_review.html
└── backend/
    └── hbnb/
        ├── app/
        │   ├── api/v1/
        │   │   ├── auth.py
        │   │   ├── users.py
        │   │   ├── places.py
        │   │   ├── reviews.py
        │   │   └── amenities.py
        │   ├── models/
        │   │   ├── base_model.py
        │   │   ├── user.py
        │   │   ├── place.py
        │   │   ├── review.py
        │   │   └── amenity.py
        │   ├── persistence/
        │   │   └── repository.py
        │   ├── services/
        │   │   └── facade.py
        │   └── __init__.py
        ├── config.py
        ├── schema.sql
        ├── initial_data.sql
        ├── requirements.txt
        └── run.py
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- pip
- Git
- VS Code + Live Server extension

### Full Setup

```bash
# 1. Clone
git clone https://github.com/Ali731-Amb/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4

# 2. Setup backend
cd backend/hbnb
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Initialize database
sqlite3 instance/hbnb_dev.db < schema.sql
sqlite3 instance/hbnb_dev.db < initial_data.sql

# 4. Start backend
python3 run.py
# → API running at http://127.0.0.1:5000
# → Swagger UI at http://127.0.0.1:5000/api/v1/

# 5. Open frontend
# Open frontend/index.html with Live Server in VS Code
# → Frontend running at http://localhost:5500
```

---

## API Reference

### Auth
```
POST /api/v1/auth/login
Body: { "email": "...", "password": "..." }
Response: { "access_token": "eyJ..." }
```

### Places
```
GET  /api/v1/places/              → List all places
GET  /api/v1/places/<id>          → Get place with owner + reviews
POST /api/v1/places/              → Create place (JWT required)
PUT  /api/v1/places/<id>          → Update place (owner only)
```

### Reviews
```
GET  /api/v1/reviews/             → List all reviews
POST /api/v1/reviews/             → Create review (JWT required)
PUT  /api/v1/reviews/<id>         → Update review (author only)
DELETE /api/v1/reviews/<id>       → Delete review (author only)
```

### Users
```
GET  /api/v1/users/               → List all users
GET  /api/v1/users/<id>           → Get user by ID
PUT  /api/v1/users/<id>           → Update own profile (JWT required)
POST /api/v1/users/users/         → Create user (admin JWT required)
PUT  /api/v1/users/users/<id>     → Update any user (admin JWT required)
```

---

## Test Data

### Users

| Role  | Email                  | Password   | ID                                     |
|-------|------------------------|------------|----------------------------------------|
| Admin | admin@hbnb.io          | Admin1234! | `36c9050e-ddd3-4c3b-9731-9f487208bbc1` |
| User  | john@test.com          | Test1234!  | `26f8a71b-4dc4-466f-9bff-e16fd9237c25` |
| User  | jane@test.com          | Test1234!  | `e9609afd-a6e8-4c4c-903d-aeeefbd4891f` |

### Places (owned by John)

| Title                 | Price | ID                                     |
|-----------------------|-------|----------------------------------------|
| Beautiful Beach House | $150  | `df41dbf1-e0f5-4168-8f59-6a336b48f9aa` |
| Cozy Cabin            | $80   | `beabb4be-485b-45cd-818e-8c8c24f3da66` |
| Modern Apartment      | $200  | `437d8c64-7c04-42d9-83a4-3b2f92112f53` |
| Lieu admin            | $100  | `99271eb3-655a-4f91-ad34-9dee7545387c` |

### Amenities

| Name            | ID                                     |
|-----------------|----------------------------------------|
| WiFi            | `467073a3-b3c0-4c1f-9831-5467a67dcea5` |
| Piscine         | `160cb549-80bc-4f3d-9184-5bd98a914c24` |
| Climatisation   | `b6b08f7c-e8c0-48fd-9acf-d265d19fe09d` |

---

## Note on CORS

The frontend runs on port `5500` (Live Server) and the backend on port `5000` (Flask).  
CORS is configured in `backend/hbnb/app/__init__.py`:

```python
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
```

All fetch URLs in `scripts.js` use absolute URLs:
```javascript
fetch('http://127.0.0.1:5000/api/v1/places/', ...)
```

---

## Author

**Alison Amblard**  
Student at Holberton School — Cohort 2024  
GitHub: [Ali731-Amb](https://github.com/Ali731-Amb)  
Project: HBnB Evolution — Parts 1 to 4
