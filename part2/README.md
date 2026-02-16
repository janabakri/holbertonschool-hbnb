HBnB Project – Part 2: RESTful API Implementation
1. Project Overview
What is HBnB?

HBnB is a simplified clone of Airbnb, developed as part of the Holberton School curriculum.
This is Part 2 of the project, where the focus is on implementing a fully functional RESTful API that serves as the backend of the application.

The system manages users, property listings, reviews, and amenities while applying clean architecture principles and software design patterns to ensure scalability, maintainability, and security.

Purpose

The API allows users to:

Manage Users – Register, view, and update user profiles

List Properties – Create and manage property listings

Write Reviews – Rate and review properties

Add Amenities – Define property features

This backend is designed to be easily extendable and ready for database integration in Part 3.

Key Features

Complete CRUD operations for all entities

Input validation and structured error handling

Password hashing for secure storage

UUID-based unique identifiers

Swagger documentation (auto-generated)

Comprehensive test suite using pytest

Clean architecture with clear separation of concerns

Modular and scalable codebase

2. System Architecture

The project follows a Three-Layer Architecture, ensuring proper separation between responsibilities.

2.1 Three-Layer Architecture
1️⃣ Presentation Layer

Built using Flask and Flask-RESTx

Defines API endpoints

Handles HTTP requests and responses

Performs request parsing and validation

Returns structured JSON responses

Provides automatic Swagger documentation

This layer does not contain business logic.

2️⃣ Business Logic Layer

Contains models:

User

Place

Review

Amenity

Implements business rules

Applies validation logic

Ensures relationships between entities

Hashes passwords before storage

This layer guarantees data consistency and enforces application rules.

3️⃣ Persistence Layer

Implements an in-memory repository

Stores objects in dictionary-based storage

Provides CRUD operations (create, retrieve, update, delete)

This layer is isolated and can be replaced by a real database in Part 3 without modifying higher layers.

3. Design Patterns Used
3.1 Facade Pattern

The HBnBFacade class provides a simplified interface to the internal system components.

Instead of interacting directly with models and repositories, the API communicates with the facade, which handles validation, object creation, and storage internally.

Benefits:

Reduces coupling between layers

Simplifies API logic

Improves maintainability

Makes database integration easier

3.2 Repository Pattern

The repository pattern abstracts data storage from business logic.

Benefits:

Clear separation of concerns

Easier unit testing

Replaceable storage mechanism

Improved modularity

4. Core Functionalities
User Management

Create users

Retrieve user information

Update user profiles

Secure password hashing

Email uniqueness validation

Place Management

Create property listings

Retrieve place details

Update listing information

Associate places with owners

Link amenities

Review Management

Create reviews

Associate reviews with users and places

Retrieve reviews by place

Enforce rating constraints

Amenity Management

Create amenities

List amenities

Associate amenities with places

5. Technologies Used
Technology	Purpose	Why Used
Python	Programming Language	Industry standard for backend development
Flask	Web Framework	Lightweight and flexible
Flask-RESTx	API Development	Swagger documentation and request parsing
pytest	Testing	Powerful and flexible testing framework
pytest-cov	Coverage	Measures test coverage
UUID	ID Generation	Ensures unique identifiers
hashlib	Password Hashing	Secure password storage
6. Testing Strategy

Unit tests written using pytest

Separate test files for each entity

CRUD operations fully tested

Validation and error scenarios covered

Coverage measured using pytest-cov

This ensures system reliability and prevents regressions.

7. Project Structure

holbertonschool-hbnb/ └── part2/ ├── app/ │ ├── __init__.py # Application factory │ ├── api/ │ │ ├── __init__.py │ │ └── v1/ │ │ ├── __init__.py │ │ ├── users.py # User endpoints │ │ ├── places.py # Place endpoints │ │ ├── reviews.py # Review endpoints │ │ └── amenities.py # Amenity endpoints │ ├── models/ │ │ ├── __init__.py │ │ ├── user.py # User model │ │ ├── place.py # Place model │ │ ├── review.py # Review model │ │ └── amenity.py # Amenity model │ ├── persistence/ │ │ ├── __init__.py │ │ └── repository.py # In-memory repository │ └── services/ │ ├── __init__.py │ └── facade.py # Facade pattern ├── tests/ │ ├── __init__.py │ ├── test_users.py # User tests │ ├── test_places.py # Place tests │ ├── test_reviews.py # Review tests │ └── test_amenities.py # Amenity tests ├── requirements.txt # Dependencies ├── run.py # Entry point └── README.md # Documentation ---

8. Team Members

Rama Alshehri

Jana Bakri

Raghad AlMalki

9. Project Strengths

Clean and modular architecture

Clear separation of concerns

Industry-standard design patterns

Secure password handling

Comprehensive API documentation

High test coverage

Scalable and maintainable design
