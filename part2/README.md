# HBnB Project - Part 2: RESTful API Implementation

## Project Overview
HBnB is a simplified clone of Airbnb, developed as part of the Holberton School curriculum. This is Part 2 of the project, focusing on implementing a fully functional RESTful API that serves as the backend of the application.

The system manages users, property listings, reviews, and amenities while applying clean architecture principles and software design patterns to ensure scalability, maintainability, and security.

## Purpose
The API allows users to:

- **Manage Users**: Register, view, and update user profiles
- **List Properties**: Create and manage property listings
- **Write Reviews**: Rate and review properties
- **Add Amenities**: Define property features

This backend is designed to be easily extendable and ready for database integration in Part 3.

## Key Features
- Complete CRUD operations for all entities
- Input validation and structured error handling
- Password hashing for secure storage
- UUID-based unique identifiers
- Swagger documentation (auto-generated)
- Comprehensive test suite using pytest
- Clean architecture with clear separation of concerns
- Modular and scalable codebase

## System Architecture

The project follows a **Three-Layer Architecture**, ensuring proper separation between responsibilities.

### 2.1 Presentation Layer
- Built using **Flask** and **Flask-RESTx**
- Defines API endpoints
- Handles HTTP requests and responses
- Performs request parsing and validation
- Returns structured JSON responses
- Provides automatic Swagger documentation

### 2.2 Business Logic Layer
- Contains models: **User, Place, Review, Amenity**
- Implements business rules
- Applies validation logic
- Ensures relationships between entities
- Hashes passwords before storage
- Guarantees data consistency and enforces application rules

### 2.3 Persistence Layer
- Implements an **in-memory repository**
- Stores objects in dictionary-based storage
- Provides CRUD operations: create, retrieve, update, delete
- Isolated layer that can be replaced by a real database in Part 3 without modifying higher layers

## Design Patterns Used

### 3.1 Facade Pattern
Located in `app/services/facade.py`, the Facade provides a simplified interface to the internal system components, handling validation, object creation, and storage internally.

**Benefits:**
- Reduces coupling between layers
- Simplifies API logic
- Improves maintainability
- Eases database integration

### 3.2 Repository Pattern
Located in `app/persistence/repository.py`, the Repository abstracts data storage from business logic.

**Benefits:**
- Clear separation of concerns
- Easier unit testing
- Replaceable storage mechanism
- Improved modularity

## Core Functionalities

### User Management
- Create users
- Retrieve user information
- Update user profiles
- Secure password hashing
- Email uniqueness validation
