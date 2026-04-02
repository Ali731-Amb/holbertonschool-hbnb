# HBnB Evolution: Production-Ready AirBnB Clone API

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)
![Flask-RESTX](https://img.shields.io/badge/Flask--RESTX-1.x-orange.svg)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)
![JWT](https://img.shields.io/badge/Auth-JWT-yellow.svg)

---

## Overview

HBnB Evolution is a RESTful API inspired by AirBnB, designed with a multilayered architecture and built for scalability.

This version introduces:
- JWT-based authentication
- Role-based access control (RBAC)
- Persistent storage using SQLAlchemy
- Transition from in-memory storage to relational databases

---

## Technical Stack

- Backend: Flask, Flask-RESTX
- Authentication: Flask-JWT-Extended
- ORM: SQLAlchemy
- Database:
  - Development: SQLite
  - Production: MySQL-ready
- Security: Bcrypt (password hashing)

---

## Architecture

The project follows a strict separation of concerns:

- API Layer: Handles HTTP requests, validation, serialization
- Service Layer: Business logic and rules
- Repository Layer: Data persistence abstraction
- Facade Layer: Central orchestration point

Key Patterns:
- Repository Pattern
- Facade Pattern

---

## Authentication & Security

### Authentication Flow

1. User logs in
2. Server validates credentials
3. JWT token is generated
4. Client sends token in headers for protected routes

Example header:

Authorization: Bearer <JWT_TOKEN>

---

### Authorization Rules

- Users can:
  - Modify their own data
  - Create and manage their places and reviews

- Admins can:
  - Manage all users
  - Manage amenities
  - Bypass ownership checks

---

## Database Design

### ORM Mapping

All entities are mapped using SQLAlchemy:

- User
- Place
- Review
- Amenity

### Relationships

- One-to-Many:
  - User → Places
  - User → Reviews
  - Place → Reviews

- Many-to-Many:
  - Place ↔ Amenity

---

## Data Integrity Constraints

- Unique email per user
- Passwords hashed (bcrypt)
- No password exposure in API responses
- A user cannot:
  - Review their own place
  - Review the same place twice

---

## Persistence Layer Evolution

Previous:
- In-memory repository

Current:
- SQLAlchemy repository implementation

Impact:
- Persistent data
- Scalable architecture
- Production-ready design

---

## Installation

git clone https://github.com/your-username/hbnb-evolution.git  
cd hbnb-evolution  

python3 -m venv venv  
source venv/bin/activate  

pip install -r requirements.txt  

---

## Running the Application

python run.py  

Base URL: http://127.0.0.1:5000  

Swagger documentation available at runtime.

---

## API Overview

### Authentication

POST /api/v1/auth/login  
→ returns JWT token  

---

### Users

- POST /users → admin only
- GET /users → admin only
- GET /users/<id> → authenticated
- PUT /users/<id> → owner or admin

---

### Places

- POST /places → authenticated
- PUT /places/<id> → owner or admin
- DELETE /places/<id> → owner or admin

---

### Reviews

- POST /reviews → authenticated
- PUT /reviews/<id> → owner
- DELETE /reviews/<id> → owner or admin

---

### Amenities

- POST /amenities → admin only
- PUT /amenities/<id> → admin only
- GET /amenities → public

---

## Example Request Flow (Conceptual)

1. Login → get token  
2. Create place → send token  
3. Add review → send token  
4. Unauthorized action → rejected (403)

---

## Testing Strategy

- Manual testing via:
  - Swagger UI
  - Postman
  - curl

Focus:
- Authentication
- Authorization
- Data integrity
- Edge cases

---

## Database Visualization

Entity-Relationship diagram created using Mermaid.js  
(see project documentation folder)

---

## Future Improvements

- Dockerization
- CI/CD integration
- Automated testing (pytest)
- Rate limiting
- Caching layer

---

## Author

AMBLARD Alison

---

## License

MIT