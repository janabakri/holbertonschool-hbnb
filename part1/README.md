### 0. High-Level Package Diagram
## Overview
This package diagram shows the three-layer architecture of the HBnB Evolution application and how layers communicate through the Facade design pattern.

---
## Package Diagram

<img width="4792" height="4345" alt="User Place Review Platform-2026-02-05-162012" src="https://github.com/user-attachments/assets/065a3afd-5b53-4a4b-a13c-af7bc9422040" />


### Architecture Layers
## Layer 1: Presentation Layer
*Responsibility:* Handle user interaction, HTTP requests/responses, input validation, and response formatting.

*Components:*
- *API:* RESTful endpoints (UserAPI, PlaceAPI, etc.) that receive HTTP requests
- *Services:* Interface defining contracts for business operations

## Layer 2: Business Logic Layer
*Responsibility:* Contains core business rules, validation logic, and entity management.

*Components:*
- *HbnbFacade:* Implements Facade Pattern - provides simplified interface to complex system
- *Models:* Your User, Place, Review, Amenity classes with business logic

## Layer 3: Persistence Layer
*Responsibility:* Data storage, retrieval, and database operations.

*Components:*
- *Repositories:* Data access abstraction layer
- *Database:* External storage system (PostgreSQL/MySQL)

## Facade Pattern Communication Flow
The Facade Pattern simplifies communication between layers by:
1. *Presentation Layer* calls simple methods on HbnbFacade
2. *HbnbFacade* internally coordinates between multiple models
3. *HbnbFacade* calls repositories for data persistence
4. Complex interactions are hidden behind a simple interface

Example: Instead of API → UserModel → PlaceModel → Repository,
the flow becomes: API → HbnbFacade → (internal coordination) → Repository


---
