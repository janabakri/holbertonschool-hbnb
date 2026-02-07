## HBnB Evolution — System Architecture & Design Documentation Overview

**This document provides a comprehensive technical overview of the HBnB Evolution system architecture, focusing on package structure, business logic design, entity relationships, and API interaction workflows. It serves as a reference for understanding how the system is organized internally and how its components collaborate to deliver core functionality.**

## The documentation includes:

-A high-level package diagram illustrating the three-layer architecture and Facade communication flow

-A detailed class diagram for the Business Logic layer

-Explicit business rules and multiplicity constraints for all core entities

-Sequence diagrams demonstrating how key API operations are executed across system layers

This document is intended for developers, reviewers, and instructors who need a clear and structured understanding of the system’s internal design prior to implementation.

---
## Contributors

Raghad Almalki — https://github.com/Raghad717

Rama Alshahri — https://github.com/csrama

Jana Bakri — https://github.com/janabakri

---


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
### 1. Detailed Class Diagram for Business Logic Layer

## This document presents a detailed class diagram for the HBnB (Home Booking System) Business Logic Layer. The diagram illustrates the core domain entities, their attributes, methods, and relationships that form the foundation of the application's business logic.

---

## Class Diagram
![UML Diagram](https://www.plantuml.com/plantuml/png/hLPDRzms4Btlhz2n7rYWvo8muZGjOA27egdFn2mvAmrCSWHoA7URzh_Nr6mYKv9X7tBSzuRauvl7MRtF0abAy8VyG7641A6p7dA-5KbqAe9tbkCd-WUxdmx2OoVSdLY4G-SeeHNYU3Z0AKi2Axgq-m0PVur2Ska-7xhkHtBTpztz_Tt7-iCc145dG9x0Zo3u5mMiH1dTBd4yLZR3XDzz_yHyOFO8iM8EFSe6xL4CkHdLCnLQpfsfvG2bzVHTMYaZ530BX74kc9ZSuR_3GMzydp7fNJ40-IV-aoIAVKL6oFcHapC3vA5XpfIoc0W16zZ37ZeE75k4iW4NABRNhwWLch21LPUPCD6Pq3MS6fomfooOrBYCQPR2FSN6O0MvI8CkBes9p-HnpTe1Oe_cYnThUjPrCRF8RPVd-y1-fy_5-sgMabjpg2PJE3Lhl_Rj3myMjN52ubj_7MQRQAmHRpkHoA8PCPb8_L3J-fjd46sTa1I73SQntu3WNCASctqjoQK1ie1WMy8bIcgh0lnj-e9PwcvtKR3NtftG9UQmHa667PWV8oRJFDG04VeML4cbbJrmoMXIyTZWcYgRyDeuzNf9ohgPOpbvoiCcLl450f8TQDe63RmjNfD8TgONr-s0zi701EJXH9xaijdLEGC1umwLCF24BTjcKId2F9E_KvPtjrfzywKauKJu-ApWpnduoiE42Neq2OHYlwXV8giBDBDQrNRISWWOfMbHoUi-ZhKPBMJhLJn5pAjiWBKbWRripocHB0XnR2dFU-W4lc0BKTwVI9liwANRyBpoJw0dKblTPcHhixBHe2DfLgdOHvA1Odtwn6wRZv6JxC-PQmoqQn72smQD1S6ULy-TR5jLTMM1w22vJPQfxWdUMCxBdDhnzwhlsnYiIPuJzYpey_E_kGgcQ7rnw7RTgi13pVNdvSrINFqfAyn5LlZU91GMy3eF5XFQMVRsXx8rxoftHZcUAOLjuA95_t8CPu5xewgQcrzoNQV-XXuJMypPZ7096FTYh78yd3ok6_3iq-tTlyUZVjXKCmTC97NTfcHkx2ir-dvVARg6y9MggzkhgiCiz8TdSdxXC7AU7u2In-FDekCsPxO4Cwihta0l0gzyk_cYR7_vFdzuZz7L3_3_0G00)

### Explanatory Notes
*1. BaseEntity*
Role: Abstract base class providing common functionality to all domain entities.

## Key Attributes & Methods:

id (UUID): Unique identifier for each entity

created_at, updated_at: Audit trail timestamps

save(), delete(): Persistence operations

update_timestamp(): Updates the updated_at field automatically

Design Purpose: Implements the Template Method Pattern to ensure consistent behavior across all entities (DRY principle).

*2. User Entity*
Role: Represents all system users (guests, hosts, administrators).

## Key Business Logic:

Authentication: login(), logout(), change_password()

Authorization: is_administrator() determines access levels

Profile Management: update_profile(), get_full_name()

Account Lifecycle: register(), deactivate(), verify_email()

Critical Business Rules:

Only verified emails can create bookings

Administrative users have elevated privileges

Inactive users cannot log in

3. Place Entity
Role: Represents rental properties available for booking.

## Key Business Logic:

Lifecycle Management: create(), publish(), unpublish(), archive()

Pricing & Availability: calculate_price(), check_availability()

Amenity Management: add_amenity(), remove_amenity(), get_amenities()

Review System: get_reviews(), get_average_rating()

Critical Business Rules:

Only published places are visible to guests

Price calculations consider amenities and seasonal rates

Availability checks prevent double bookings

*4. Review Entity*
Role: Manages user reviews and ratings for places.

## Key Business Logic:

Rating System: calculate_rating() aggregates sub-ratings (cleanliness, accuracy, etc.)

Validation: validate(), is_within_period() (ensures timely reviews)

Moderation: report(), can_edit() (user permission checks)

Critical Business Rules:

Users can only review places they've booked

Verified stays get priority in display

Reviews can only be edited within a limited timeframe

*5. Amenity Entity*
Role: Defines features and facilities available at places.

## Key Business Logic:

Categorization: Organizes amenities by type (kitchen, bathroom, etc.)

Pricing Logic: is_included() vs. additional_cost

Place Association: get_places() finds all places offering this amenity

Critical Business Rules:

Standard amenities are included in base price

Additional amenities incur extra charges

Amenities can be activated/deactivated per place

*6. Booking Entity*
   
Role: Manages reservation transactions between users and places.

## Key Business Logic:

Reservation Management: create(), confirm(), cancel()

Validation: check_dates(), validate_guests(), is_cancellable()

Financial Operations: calculate_total(), process_payment()

Critical Business Rules:

Bookings must respect place capacity limits

Cancellation policies affect refund eligibility

Dates must be sequential (check-in before check-out)

---

###  Multiplicity Constraints

## 1. User → Place (1 to Many)
Constraint: One User can own/manage many Places

Database Enforcement:

Foreign key constraint: owner_id in places table references users.id

Cascade delete: When a User is deleted, their owned Places may be archived rather than deleted

Index on owner_id for fast querying of User's Places

Business Logic Enforcement:

Before creating a Place: Verify User exists and is active

Before transferring ownership: Validate new owner is eligible (not banned, verified, etc.)

Place lifecycle tied to User status: If User is deactivated, their Places are automatically unpublished

## 2. Place → Review (1 to Many)
Constraint: One Place can receive many Reviews

Database Enforcement:

Foreign key constraint: place_id in reviews table references places.id

Index on place_id for retrieving all reviews of a Place

Trigger to update places.review_count and places.rating_average on Review changes

Business Logic Enforcement:

Review creation: Must verify the reviewer actually stayed at the Place (check Booking records)

Review period: Reviews can only be submitted within 30 days of check-out

One-review-per-stay: Check if User already reviewed this specific Booking

Moderation system: New reviews go through automated and manual moderation

## 3. User → Review (1 to Many)
Constraint: One User can write many Reviews

Database Enforcement:

Foreign key constraint: user_id in reviews table references users.id

Index on user_id for retrieving User's review history

Unique constraint: (user_id, booking_id) to enforce one review per booking

Business Logic Enforcement:

Identity verification: Ensure User is who they claim to be (email verification, phone verification)

Review credibility: Track verified stays vs unverified reviews

Rate limiting: Prevent review spamming (max 3 reviews per week per user)

Reputation system: User's overall rating affects review weight

## 4. Place ↔ Amenity (Many to Many)
Constraint: Many Places can have many Amenities

Database Enforcement:

Junction table: place_amenities with columns place_id, amenity_id, additional_cost, is_included

Composite primary key: (place_id, amenity_id)

Foreign keys to both places and amenities tables

Indexes on both foreign keys for bidirectional querying

Business Logic Enforcement:

Amenity validation: Check if amenity is active before adding to Place

Pricing logic: Standard amenities have additional_cost = 0 and is_included = true

Availability checking: Some amenities may be seasonal (only available certain months)

Categorization: Group amenities for display and filtering purposes

## 5. User → Booking (1 to Many)
Constraint: One User can make many Bookings

Database Enforcement:

Foreign key constraint: user_id in bookings table references users.id

Index on user_id for retrieving User's booking history

Check constraint: guests > 0 and check_out > check_in

Trigger to validate availability before insert/update

Business Logic Enforcement:

Booking limits: Maximum 3 active bookings per User at a time

Payment verification: Must have valid payment method on file

Cancellation history: Track cancellation rate (Users with high rates may face restrictions)

Age verification: Minimum age requirement for booking certain properties

Review requirement: Must review past stays before making new bookings (optional rule)

## 6. Place → Booking (1 to Many)
Constraint: One Place can have many Bookings

Database Enforcement:

Foreign key constraint: place_id in bookings table references places.id

Index on place_id for retrieving Place's booking history

Exclusion constraint: Prevent overlapping bookings for same Place

Check constraint: guests <= places.max_guests

Business Logic Enforcement:

Availability window: Place owners can set advance booking window (e.g., 12 months max)

Minimum stay: Enforce minimum nights requirement

Blackout dates: Allow owners to block specific dates

Dynamic pricing: Adjust price based on season, demand, length of stay

Preparation time: Ensure minimum gap between bookings for cleaning
                   explain it better or add on it to be more spesific






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

## Project Team
- *Raghad Almalki*    
- *Rama Alshahri* 
- *Jana Bakri* 
