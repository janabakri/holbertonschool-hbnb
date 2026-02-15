# 🏨 HBnB Project - Part 2: RESTful API Implementation

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Flask-RESTx](https://img.shields.io/badge/Flask--RESTx-1.1.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Team Members](#team-members)
- [Technologies Used](#technologies-used)
- [Project Architecture](#project-architecture)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Complete API Endpoints](#complete-api-endpoints)
- [Data Models](#data-models)
- [Testing Guide](#testing-guide)
- [Features Implemented](#features-implemented)
- [Error Handling](#error-handling)
- [Validation Rules](#validation-rules)
- [Contributors](#contributors)
- [License](#license)

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
- ✅ Complete CRUD operations for all entities
- ✅ Input validation and error handling
- ✅ Password hashing for security
- ✅ Swagger documentation
- ✅ Comprehensive test suite
- ✅ Clean architecture with separation of concerns

### Architecture
The project follows a **3-layer architecture**:
1. **Presentation Layer** - API endpoints using Flask-RESTx
2. **Business Logic Layer** - Models and business rules
3. **Persistence Layer** - In-memory repository (to be replaced with database in Part 3)

---

## 2. Team Members

| Name | Role | GitHub | Contributions |
|------|------|--------|---------------|
| **Rama Alshehri** | Lead Developer | [@rama-alshehri](https://github.com/rama-alshehri) | Project architecture design, User and Place models, API endpoint development, Repository pattern |
| **Jana Bakri** | Backend Developer | [@jana-bakri](https://github.com/jana-bakri) | Review and Amenity models, Facade pattern, Validation logic, Testing framework |
| **Raghad Al-Malki** | API Specialist | [@raghad-almalki](https://github.com/raghad-almalki) | Flask-RESTx integration, Swagger documentation, Error handling, API testing |

---

## 3. Technologies Used

| Technology | Version | Purpose | Why Used? |
|------------|---------|---------|-----------|
| **Python** | 3.8+ | Programming Language | Industry standard for web APIs |
| **Flask** | 2.3.3 | Web Framework | Lightweight, flexible, excellent for REST APIs |
| **Flask-RESTx** | 1.1.0 | API Development | Automatic Swagger docs, request parsing |
| **pytest** | 7.4.0 | Testing | Powerful testing framework |
| **pytest-cov** | 4.1.0 | Coverage | Measure test coverage |
| **UUID** | Built-in | ID Generation | Universally unique identifiers |
| **hashlib** | Built-in | Password Hashing | Secure password storage |

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
Team Members
Name	Role
Rama Alshehri	
Jana Bakri	
Raghad Al-Malki
