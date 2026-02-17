
## Introduction: HBnB Evolution

**HBnB Evolution is a modern hospitality platform designed to facilitate secure, scalable, and efficient short-term accommodation booking. Built on clean software architecture principles, the system connects hosts and guests through a reliable and well-structured digital ecosystem while ensuring maintainability, performance, and extensibility.**

*This document presents the technical architecture and design foundations that support both current system requirements and future evolution.*

---

## HBnB Evolution: Architectural Overview
---
**System Architecture**
HBnB Evolution follows a three-layer architecture designed for scalability, maintainability, and clean separation of concerns. The system implements the Facade Pattern to simplify complex interactions between components.

---
## Architectural Layers

1. Presentation Layer
Purpose: Handles all user interactions and HTTP communications

Components:

RESTful API endpoints (UserAPI, PlaceAPI, ReviewAPI, etc.)

Request/Response processing and validation

JSON/XML formatting and error handling

Responsibility: User interface, input sanitization, and response delivery

## 2. Business Logic Layer
Purpose: Contains core business rules and entity management

Key Component: HbnbFacade - A simplified interface coordinating complex operations

Entities:

User: Authentication, authorization, profile management

Place: Property listings, availability, pricing logic

Review: Rating system, validation, moderation

Booking: Reservation management, financial operations

Amenity: Property features and facilities

Responsibility: Business rules validation, entity coordination, workflow management

## 3. Persistence Layer
Purpose: Manages data storage and retrieval

Components:

Repositories: Data access abstraction (UserRepository, PlaceRepository, etc.)

Database: PostgreSQL/MySQL with optimized schema

Responsibility: Data persistence, query optimization, transaction management

Communication Flow
The system uses a simplified request flow through the Facade Pattern:

API Request → HbnbFacade → [Business Logic Coordination] → Repository → Database

Instead of API calling multiple models and repositories directly, we use API calls simple Facade methods that handle complex coordination internally.

## Core Business Entities
BaseEntity (Template Method Pattern)
Purpose: Foundation for all domain entities

Features:

UUID-based unique identifiers

Automatic audit trails (created_at, updated_at)

Consistent CRUD operations

Design Principle: DRY (Don't Repeat Yourself) across all entities

User Management
Roles: Guests, Hosts, Administrators

## Key Features:

Multi-factor authentication

Role-based access control

Profile and account lifecycle management

Security: Email verification, password policies, session management

## Place Management

Lifecycle: Creation → Publication → Booking → Archiving

Features:

Dynamic pricing with seasonal rates

Real-time availability checking

Amenity-based categorization

## Review and rating aggregation

Rules: Only published places are bookable; owners control availability

Review System
Validation: Verified stays only, time-bound submissions

Structure: Multi-criteria ratings (cleanliness, accuracy, etc.)

Moderation: Automated and manual review processes

Integrity: One review per verified booking

## Booking Engine

Reservation Logic: Date validation, capacity checks, pricing calculations

Financial Operations: Payment processing, refund calculations

Policies: Cancellation rules, minimum stay requirements

Validation: Prevents overlapping bookings, enforces house rules

## Amenity Management

Categorization: Kitchen, bathroom, entertainment, etc.

Pricing: Included vs. additional-cost amenities

Association: Many-to-many relationship with places

Filtering: Enables advanced property search

## Entity Relationships & Constraints

**Key Relationships**

User → Place (1:Many): Owners manage multiple properties


Place → Review (1:Many): Properties receive multiple reviews


User → Review (1:Many): Users write multiple reviews


Place ↔ Amenity (Many:Many): Properties offer multiple amenities


User → Booking (1:Many): Users make multiple reservations


Place → Booking (1:Many): Properties host multiple bookings

## Business Rule Enforcement

Data Integrity: Foreign key constraints, unique constraints, check constraints

Temporal Rules: Review windows, booking advance limits, cancellation periods

Quantitative Limits: Maximum concurrent bookings, review frequency limits

State Management: User activation, place publication status, booking states


## API Workflow Examples

**1. User Registration**

Client → API → Service → Facade → [User Validation] → Repository → Database

Key Steps: Email uniqueness check, password hashing, verification email

Validation: Duplicate prevention, data integrity, security compliance

**2. Place Creation**

Client → API → Service → Facade → [Owner Verification + Place Validation] → Repository → Database

Key Steps: Owner authentication, place data validation, amenity association

Validation: Owner eligibility, pricing rules, amenity compatibility

**3. Review Submission**

Client → API → Service → Facade → [Booking Verification + Review Validation] → Repository → Database

Key Steps: Verified stay confirmation, duplicate review prevention, rating calculation

Validation: Stay verification, time window compliance, content moderation

**4. Place Search**

Client → API → Service → Facade → [Filter Processing] → Repository → [Database Query] → Response Assembly

Key Steps: Filter parsing, availability checking, amenity matching

Optimization: Pagination, caching, eager loading of amenities

## Design Principles

**SOLID Compliance**

Single Responsibility: Each class has one reason to change

Open/Closed: Extensible without modification

Liskov Substitution: Derived classes substitutable for base classes

Interface Segregation: Client-specific interfaces

Dependency Inversion: Depend on abstractions, not concretions

## Patterns Implemented

Facade Pattern: Simplified interface to complex subsystem

Template Method Pattern: Consistent entity lifecycle in BaseEntity

Repository Pattern: Abstract data access layer

Strategy Pattern: Pluggable pricing and validation algorithms

## Performance Considerations

**Database Optimization**

Indexing: Foreign keys, frequently queried fields

Partitioning: Temporal data (reviews, bookings) by date

Caching: Frequently accessed places, user sessions

Connection Pooling: Efficient database connection management

## API Performance

Pagination: Large result sets divided into pages

Lazy Loading: Related entities loaded on demand

Response Compression: Reduced bandwidth usage

Rate Limiting: API endpoint protection

## Security Measures

**Authentication & Authorization**

JWT Tokens: Stateless session management

Role-Based Access: Granular permission control

Input Validation: SQL injection prevention, XSS protection

Data Encryption: Sensitive data at rest and in transit

## Business Logic Security

Ownership Verification: Users can only modify their own resources

State Transitions: Controlled entity state changes

Financial Integrity: Auditable booking and payment trails

Content Moderation: Review and messaging oversight

## Scalability Features

Horizontal Scaling

Stateless API Layer: Easy replication

Database Read Replicas: Load distribution

Caching Layer: Redis/Memcached for frequent queries

Message Queues: Asynchronous processing for emails, notifications

Microservices Readiness
Clear Bounded Contexts: Natural service boundaries

API-First Design: RESTful, versioned endpoints

Event-Driven Architecture: Placeholder for future event bus implementation

## Monitoring & Maintenance 
Observability
Logging: Structured logging for debugging and audit trails

Metrics: API response times, database query performance

Health Checks: System component availability monitoring

Alerting: Proactive issue detection and notification

Maintenance Features
Database Migrations: Version-controlled schema changes

Backup Strategy: Regular data backups with point-in-time recovery

Deployment Pipeline: CI/CD for consistent releases

Feature Flags: Gradual feature rollouts and A/B testing

Integration Points
External Services
Payment Gateways: Stripe/PayPal integration for transactions

Email Service: SendGrid/Mailgun for notifications

SMS Service: Twilio for two-factor authentication

Mapping Service: Google Maps/Mapbox for location services

## Third-Party APIs
Identity Verification: Background checks for hosts

Payment Processing: Secure transaction handling

Review Aggregation: Cross-platform reputation import

Analytics Integration: Usage tracking and business intelligence

*This architecture provides a robust foundation for HBnB Evolution, balancing flexibility with structure, and enabling both current functionality and future growth. The clear separation of concerns, consistent patterns, and comprehensive validation ensure a maintainable, scalable, and secure platform for property rentals and bookings.*

## Contributors 

- *Raghad Almalki* – https://github.com/Raghad717  
- *Rama Alshahri* – https://github.com/csrama  
- *Jana Bakri* – https://github.com/janabakri

- # HBnB - RESTful API Backend

- ## Overview

HBnB is a simplified Airbnb-like backend system developed as part of the Holberton School curriculum. This project implements a fully functional RESTful API that manages users, places, reviews, and amenities using clean architecture principles and industry best practices.

## Features

- Full CRUD operations for all resources
- Structured JSON responses with consistent formatting
- Comprehensive input validation and error handling
- Secure password hashing using hashlib
- UUID-based identifiers for all resources
- Swagger API documentation for easy testing
- Modular and scalable three-layer architecture
- Unit tests with pytest for reliability

## Architecture

The project follows a Three-Layer Architecture pattern:

| Layer | Responsibility | Key Components |
|-------|----------------|-----------------|
| Presentation | API endpoints and request handling | Flask routes, request parsing, response formatting |
| Business Logic | Core rules and validations | Data validation, business rules, authorization |
| Persistence | Data storage and retrieval | In-memory storage, data models, CRUD operations |

## Technologies

- Python 3.8+ - Core programming language
- Flask - Lightweight web framework
- Flask-RESTx - API documentation and validation
- Pytest - Unit testing framework
- UUID - Unique identifier generation
- hashlib - Password hashing and security

# Project Structure

- holbertonschool-hbnb/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── places.py
│   │   ├── reviews.py
│   │   └── amenities.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   │
│   └── persistence/
│       ├── __init__.py
│       └── repository.py
│
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_places.py
│   ├── test_reviews.py
│   └── test_amenities.py
│
├── requirements.txt
├── run.py
└── README.md
