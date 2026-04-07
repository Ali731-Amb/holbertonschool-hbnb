# HBnB - Web Client

## Overview

HBnB is a full-stack web application inspired by AirBnB, built as part of the Holberton School curriculum. This repository contains the front-end client (Part 4), which connects to a RESTful back-end API built with Flask and SQLAlchemy.

The client is built with HTML5, CSS3, and vanilla JavaScript (ES6). It communicates with the API using the Fetch API and manages user sessions through JWT tokens stored in cookies.

---

## Features

### Authentication
- Login form with email and password
- JWT token stored in a cookie (valid for 24 hours)
- Login link visible only when not authenticated
- Redirect to index if not authenticated on protected pages

### Index Page (`/index.html`)
- Displays all available places as cards
- Dynamically loaded from the API
- Client-side filter by maximum price (no page reload)
- Login link visible only when not authenticated

### Place Details (`/place.html?id=<place_id>`)
- Full place information: title, description, host, price, amenities
- Customer reviews with author names and star ratings
- "Add a Review" section visible only when authenticated

### Add Review (`/add_review.html?id=<place_id>`)
- Displays the place name dynamically ("Reviewing: [place name]")
- Review text + rating (1–5 stars)
- Redirects to index if not authenticated

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Markup    | HTML5                             |
| Styling   | CSS3                              |
| Scripting | JavaScript ES6 (vanilla)          |
| HTTP      | Fetch API (AJAX)                  |
| Auth      | JWT via cookies                   |
| Backend   | Flask + Flask-RESTX + SQLAlchemy  |
| Database  | SQLite                            |

---

## Project Structure

```
part4/
├── frontend/
│   ├── css/
│   │   └── styles.css          # Main stylesheet
│   ├── js/
│   │   └── scripts.js          # All client-side JavaScript
│   ├── assets/
│   │   └── logo.png            # Application logo
│   ├── index.html              # List of places
│   ├── login.html              # Login form
│   ├── place.html              # Place details + review form
│   └── add_review.html         # Add review form
└── backend/
    └── hbnb/
        ├── app/
        │   ├── api/            # Flask-RESTX namespaces (places, users, reviews, auth)
        │   ├── models/         # SQLAlchemy models (User, Place, Review, Amenity)
        │   ├── persistence/    # Repository pattern
        │   ├── services/       # Facade pattern
        │   └── __init__.py     # App factory
        ├── config.py           # App configuration
        ├── schema.sql          # Database schema
        ├── initial_data.sql    # Seed data
        └── run.py              # Application entry point
```

---

## Pages

| File              | Description                              |
|-------------------|------------------------------------------|
| `index.html`      | List of all places with price filter     |
| `login.html`      | Login form                               |
| `place.html`      | Detailed view of a specific place        |
| `add_review.html` | Form to add a review for a place         |

---

## JavaScript Architecture (`scripts.js`)

The script is organized into sections:

1. **Utilities** — `getCookie`, `getPlaceIdFromURL`, `checkAuthentication`
2. **Authentication** — `loginUser`
3. **Index page** — `fetchPlaces`, `displayPlaces`, `setupPriceFilter`
4. **Place details** — `fetchPlaceDetails`, `displayPlaceDetails`
5. **Add review** — `submitReview`
6. **Init** — `DOMContentLoaded` listener routing to the right functions

---

## API Endpoints Used

| Method | Endpoint                    | Description                  |
|--------|-----------------------------|------------------------------|
| POST   | `/api/v1/auth/login`        | Authenticate and get token   |
| GET    | `/api/v1/places/`           | List all places              |
| GET    | `/api/v1/places/<id>`       | Get place details            |
| POST   | `/api/v1/reviews/`          | Submit a new review          |
| POST   | `/api/v1/users/users/`      | Create a user (admin only)   |

---

## Authentication Flow

```
User fills login form
        ↓
POST /api/v1/auth/login
        ↓
API returns JWT token
        ↓
Token saved in cookie (path=/, 24h)
        ↓
User redirected to index.html
        ↓
On each page load: getCookie('token') checks auth state
        ↓
Token included in Authorization header for protected requests
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- pip
- Git
- Node.js (for Live Server extension in VS Code)

### Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/Ali731-Amb/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4
```

**2. Create and activate a virtual environment**
```bash
cd backend/hbnb
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Initialize the database**
```bash
sqlite3 instance/hbnb_dev.db < schema.sql
sqlite3 instance/hbnb_dev.db < initial_data.sql
```

**5. Start the backend**
```bash
python3 run.py
```

The API will be available at `http://127.0.0.1:5000`.  
The Swagger UI is available at `http://127.0.0.1:5000/api/v1/`.

**6. Open the frontend**

Open `frontend/index.html` with Live Server in VS Code.  
The frontend will be available at `http://localhost:5500`.

---

## Seed Data

The application comes with pre-loaded seed data including:

- 1 admin user
- 1 regular user (Johnny Doe)

Default credentials for testing:

| User       | Email              | Password    |
|------------|--------------------|-------------|
| Admin      | admin@hbnb.io      | Admin1234!  |
| Johnny Doe | john.doe@example.com | *(see DB)* |

To create additional test users, use the admin token via the `/api/v1/users/users/` endpoint.

---

## Test Users Created During Development

| User  | Email            | Password   | ID                                     |
|-------|------------------|------------|----------------------------------------|
| Admin | admin@hbnb.io    | Admin1234! | `36c9050e-ddd3-4c3b-9731-9f487208bbc1` |
| John  | john@test.com    | Test1234!  | `26f8a71b-4dc4-466f-9bff-e16fd9237c25` |
| Jane  | jane@test.com    | Test1234!  | `e9609afd-a6e8-4c4c-903d-aeeefbd4891f` |

## Test Places Created During Development

| Place                 | Price | ID                                     |
|-----------------------|-------|----------------------------------------|
| Beautiful Beach House | $150  | `df41dbf1-e0f5-4168-8f59-6a336b48f9aa` |
| Cozy Cabin            | $80   | `beabb4be-485b-45cd-818e-8c8c24f3da66` |
| Modern Apartment      | $200  | `437d8c64-7c04-42d9-83a4-3b2f92112f53` |
| Lieu admin            | $100  | `99271eb3-655a-4f91-ad34-9dee7545387c` |

---

## Note on CORS

The frontend runs on port `5500` (Live Server) and the backend on port `5000` (Flask). CORS is configured in `backend/hbnb/app/__init__.py` to allow all origins on `/api/v1/*`:

```python
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
```

All fetch URLs in `scripts.js` use absolute URLs (`http://127.0.0.1:5000/api/v1/...`) to ensure proper cross-origin communication.

---

## Author

**Alison Amblard**  
Student at Holberton School  
Project: Holberton - HBNB  
GitHub: [Ali731-Amb](https://github.com/Ali731-Amb)