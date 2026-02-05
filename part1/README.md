### 0. High-Level Package Diagram
## Overview
This package diagram shows the three-layer architecture of the HBnB Evolution application and how layers communicate through the Facade design pattern.

---
## Package Diagram

<img width="4792" height="4345" alt="User Place Review Platform-2026-02-05-162012" src="https://github.com/user-attachments/assets/ed5b9d41-77c2-4ecb-be14-e2c266ad4d3e" />


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
# Sequence Diagrams for API Calls

## Overview

This section presents sequence diagrams that illustrate how the HBnB application handles key API calls across the Presentation, Business Logic, and Persistence layers. Each diagram shows the flow of requests and responses between system components, helping to visualize how different layers interact to fulfill user actions.

The following API calls are covered:  
- User Registration  
- Place Creation  
- Review Submission  
- Fetching a List of Places  

Each sequence diagram is accompanied by a brief explanation describing the main steps involved in processing the request.  

---

## 1. User Registration
<img width="7250" height="5235" alt="Untitled diagram-2026-02-04-184051 (1)" src="https://github.com/user-attachments/assets/fd346cde-ddcb-49a5-9a49-e30a15db583d" />

Use Case: Register a new user in the system.  

Flow Overview:  
1. User sends POST /register request to the API.  
2. API forwards the request to the Service layer.  
3. Service calls the Facade to handle user creation.  
4. Facade creates a UserEntity and validates the data.  
5. Facade checks the email for uniqueness via Repository.  
6. Repository queries the Database and confirms the email does not exist.  
7. Facade saves the new user through the Repository.  
8. Repository inserts the user into the Database.  
9. API responds to the user.  

---

## 2. Place Creation
<img width="8192" height="5198" alt="Untitled diagram-2026-02-04-183846 (1)" src="https://github.com/user-attachments/assets/f6cf5491-258a-499e-8385-5877fd5c4bb5" />

Use Case: Owner creates a new place.  

Flow Overview:  
1. Owner sends POST /places request to the API.  
2. API forwards the request to Service.  
3. Service requests the Facade to create the place.  
4. Facade checks if the Owner exists using UserRepo.  
5. Facade creates a PlaceEntity and validates it.  
6. Facade saves the place via PlaceRepo to the Database.  
7. API responds to the user.  

---

## 3. Review Submission
<img width="8192" height="6336" alt="Untitled diagram-2026-02-04-183926 (1)" src="https://github.com/user-attachments/assets/fd00862c-42b1-4577-8181-1e7ef4089efa" />

Use Case: Guest adds a review for a place.  

Flow Overview:  
1. Guest sends POST /reviews request.  
2. API forwards the request to Service.  
3. Facade verifies that both the user and place exist.  
4. Facade checks if a review already exists for the same user and place.  
5. A new ReviewEntity is created and validated.  
6. Review is saved via ReviewRepo into the Database.  
7. API responds to the user.  

---

## 4. Fetching a List of Places
<img width="7405" height="4640" alt="Untitled diagram-2026-02-04-184019 (1)" src="https://github.com/user-attachments/assets/77b55cc6-abc0-40bc-b78f-8fd4097c42f8" />

Use Case: Browser searches for places with optional filters.  

Flow Overview:  
1. Browser sends GET /places?filters request to the API.  
2. API forwards the request to Service.  
3. Facade calls PlaceRepo.search() to retrieve matching places.  
4. For each place, Facade requests its amenities via AmenityRepo.  
5. Database returns the places and their amenities.  
6. API responds with the list of places including amenities.  

---

### Notes on Notation
- Activation bars are used to show the time a participant is active in the sequence.  
- Solid arrows (`->>`) indicate synchronous messages/calls.  
- Dashed arrows (`-->>`) indicate responses.  
- Loops and conditions are included to show repeated or conditional operations (e.g., retrieving amenities for each place).
