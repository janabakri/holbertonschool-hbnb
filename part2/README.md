# HBnB Project - Part 2: RESTful API Implementation

---

## 1. Project Overview

### What is HBnB?
HBnB is a simplified clone of Airbnb, developed as part of the Holberton School curriculum. This is **Part 2** of the project, where we implement a **RESTful API** that serves as the backend for the application.

### Purpose
The API allows users to:
- **Manage users** - Register, view, and update user profiles
- **List properties** - Create and manage property listings
- **Write reviews** - Rate and review properties
- **Add amenities** - Define property features

### Key Features
- Complete CRUD operations for all entities
- Input validation and error handling
- Password hashing for security
- Swagger documentation
- Comprehensive test suite
- Clean architecture with separation of concerns

### Architecture
The project follows a **3-layer architecture**:
1. **Presentation Layer** - API endpoints using Flask-RESTx
2. **Business Logic Layer** - Models and business rules
3. **Persistence Layer** - In-memory repository (to be replaced with database in Part 3)

---

## 2. Team Members

| Name | GitHub | Contributions |
|------|--------|---------------|
| **Rama Alshehri** |  [@csrama](https://github.com/csrama) | Project architecture design, User and Place models, API endpoint development, Repository pattern |
| **Jana Bakri** |  [@janabakri]( https://github.com/janabakri) | Review and Amenity models, Facade pattern, Validation logic, Testing framework |
| **Raghad Al-Malki** |  [@Raghad717]( https://github.com/Raghad717) | Flask-RESTx integration, Swagger documentation, Error handling, API testing |

---

## 3. Technologies Used

| Technology | Purpose | Why Used? |
|------------|-----------|----------|
| **Python** | Programming Language | Industry standard for web APIs |
| **Flask** | Web Framework | Lightweight, flexible, excellent for REST APIs |
| **Flask-RESTx** | API Development | Automatic Swagger docs, request parsing |
| **pytest** | Testing | Powerful testing framework |
| **pytest-cov** | Coverage | Measure test coverage |
| **UUID** |  ID Generation | Universally unique identifiers |
| **hashlib** |  Password Hashing | Secure password storage |

---

## 4. Project Architecture

### 4.1 Three-Layer Architecture

### 4.2 Design Patterns Used

#### Facade Pattern
The `HBnBFacade` class provides a simplified interface to the complex subsystem:
```python
# Example: Facade hides complexity
facade.create_user(data)  # Simple call
# Behind the scenes: validation → model creation → repository storage
# Easy to replace with database later
repository.add(user)
repository.get(user_id)
repository.update(user_id, data)
repository.delete(user_id)
users_ns.facade = facade  # Shared instance
places_ns.facade = facade  # Same instance

holbertonschool-hbnb/
└── part2/
    ├── app/
    │   ├── __init__.py                 # Application factory
    │   ├── api/
    │   │   ├── __init__.py
    │   │   └── v1/
    │   │       ├── __init__.py
    │   │       ├── users.py             # User endpoints
    │   │       ├── places.py            # Place endpoints
    │   │       ├── reviews.py           # Review endpoints
    │   │       └── amenities.py         # Amenity endpoints
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── user.py                   # User model
    │   │   ├── place.py                   # Place model
    │   │   ├── review.py                   # Review model
    │   │   └── amenity.py                   # Amenity model
    │   ├── persistence/
    │   │   ├── __init__.py
    │   │   └── repository.py                # In-memory repository
    │   └── services/
    │       ├── __init__.py
    │       └── facade.py                      # Facade pattern
    ├── tests/
    │   ├── __init__.py
    │   ├── test_users.py                       # User tests
    │   ├── test_places.py                       # Place tests
    │   ├── test_reviews.py                       # Review tests
    │   └── test_amenities.py                      # Amenity tests
    ├── requirements.txt                           # Dependencies
    ├── run.py                                      # Entry point
    └── README.md                                    # Documentation

---
**Team Members**
- Rama Alshehri	
- Jana Bakri	
- Raghad AlMalki
