# HBnB Database Entity-Relationship Diagram (ERD) Documentation

## Project: Holberton School HBnB
## Part 3: Database Schema Design

---

## 1. Introduction

This document presents the Entity-Relationship Diagram (ERD) for the Holberton HBnB project, a platform similar to Airbnb. The ERD visually represents the database schema, showing all entities (tables), their attributes, and the relationships between them. This diagram serves as a blueprint for the database implementation and ensures all stakeholders have a clear understanding of the data structure.

The diagram was created using **Mermaid.js**, a markdown-like syntax tool that allows for easy integration into documentation and version control platforms like GitHub.

---

## 2. Entity Descriptions

### 2.1 USER
The USER entity stores information about all platform users, including both guests and hosts.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each user |
| first_name | string | NOT NULL | User's first name |
| last_name | string | NOT NULL | User's last name |
| email | string | UNIQUE, NOT NULL | User's email address for login |
| password | string | NOT NULL | Hashed password for authentication |
| is_admin | boolean | DEFAULT false | Flag indicating if user has admin privileges |

**Relationships:**
- One user can own many places (one-to-many with PLACE)
- One user can write many reviews (one-to-many with REVIEW)

### 2.2 PLACE
The PLACE entity represents properties listed on the platform.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each place |
| name | string | NOT NULL | Name/title of the place |
| description | string | - | Detailed description of the property |
| city_id | string | FOREIGN KEY | References the City table (external) |
| user_id | string | FOREIGN KEY | References the owner (USER.id) |

**Relationships:**
- Many places belong to one user (many-to-one with USER)
- One place can receive many reviews (one-to-many with REVIEW)
- One place can have many amenities (many-to-many with AMENITY via PLACE_AMENITY)

### 2.3 REVIEW
The REVIEW entity stores user feedback about places they've visited.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each review |
| user_id | string | FOREIGN KEY | References the author (USER.id) |
| place_id | string | FOREIGN KEY | References the place being reviewed (PLACE.id) |
| text | string | NOT NULL | The review content |
| created_at | datetime | NOT NULL | Timestamp of when review was created |

**Relationships:**
- Many reviews belong to one user (many-to-one with USER)
- Many reviews belong to one place (many-to-one with PLACE)

### 2.4 AMENITY
The AMENITY entity stores available amenities that can be associated with places.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each amenity |
| name | string | UNIQUE, NOT NULL | Name of the amenity (e.g., "WiFi", "Pool") |

**Relationships:**
- One amenity can belong to many places (many-to-many with PLACE via PLACE_AMENITY)

### 2.5 PLACE_AMENITY (Junction Table)
This associative entity handles the many-to-many relationship between PLACE and AMENITY.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| place_id | string | FOREIGN KEY, COMPOSITE PK | References PLACE.id |
| amenity_id | string | FOREIGN KEY, COMPOSITE PK | References AMENITY.id |

**Composite Primary Key:** (place_id, amenity_id) - Ensures each combination is unique, preventing duplicate amenity assignments to the same place.

**Relationships:**
- Many PLACE_AMENITY records belong to one place (many-to-one with PLACE)
- Many PLACE_AMENITY records belong to one amenity (many-to-one with AMENITY)

---

## 3. Relationship Analysis

### 3.1 One-to-Many Relationships

| Relationship | Type | Description |
|--------------|------|-------------|
| USER → PLACE | One-to-Many | A user can own multiple properties, but each property has exactly one owner |
| USER → REVIEW | One-to-Many | A user can write multiple reviews, but each review has exactly one author |
| PLACE → REVIEW | One-to-Many | A place can receive multiple reviews, but each review is for exactly one place |

### 3.2 Many-to-Many Relationship

The relationship between PLACE and AMENITY is many-to-many:
- A place can have multiple amenities (WiFi, Pool, Kitchen, etc.)
- An amenity can be available in multiple places

This is implemented using the **PLACE_AMENITY** junction table, which:
- Resolves the many-to-many relationship into two one-to-many relationships
- Uses a composite primary key to ensure data integrity
- Allows for efficient querying of amenities by place and places by amenity

---

## 4. Data Integrity and Constraints

### 4.1 Primary Keys
- All entities use string-based UUIDs as primary keys for scalability and distributed system compatibility

### 4.2 Foreign Keys
- `PLACE.user_id` references `USER.id` (cascade delete behavior should be considered)
- `REVIEW.user_id` references `USER.id`
- `REVIEW.place_id` references `PLACE.id`
- `PLACE_AMENITY.place_id` references `PLACE.id`
- `PLACE_AMENITY.amenity_id` references `AMENITY.id`

### 4.3 Composite Keys
- `PLACE_AMENITY` uses a composite primary key (place_id, amenity_id) to ensure unique combinations

### 4.4 Additional Constraints
- `USER.email` should have a UNIQUE constraint
- `AMENITY.name` should have a UNIQUE constraint
- All NOT NULL constraints as specified in entity tables

---

## 5. Performance Considerations

### 5.1 Recommended Indexes
For optimal query performance, indexes should be created on:

| Table | Column(s) | Reason |
|-------|-----------|--------|
| USER | email | Used for login authentication |
| PLACE | user_id | Frequently used to find places by owner |
| PLACE | city_id | Used for location-based searches |
| REVIEW | place_id | Used to load all reviews for a place |
| REVIEW | user_id | Used to load all reviews by a user |
| PLACE_AMENITY | place_id | Used to find amenities for a place |
| PLACE_AMENITY | amenity_id | Used to find places with specific amenities |

### 5.2 Data Types Choice
- **String IDs**: Using strings for primary keys allows for UUID generation, which is preferable in distributed systems
- **Float for price**: Accommodates decimal values for accurate pricing
- **Datetime for timestamps**: Enables time-based queries and sorting

---

## 6. ERD Diagram

Below is the complete ERD created with Mermaid.js:

https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&dark=auto#R%3Cmxfile%3E%3Cdiagram%20name%3D%22Page-1%22%20id%3D%22StqiGNh74x7nWM2b9XyC%22%3E7Z3bcts4EoafxrU7F5PiUYfL2HEmmXGyLjne2Vy5EBGWOEuRGpCK7Tz9gAdIokzQHZmQ6HZXpWITpiAK%2FbH14yfYPHHPFve%2FCbacf0oCHp04VnB%2F4r47cRzPtiz5I295KFvskeWVLTMRBlXbpuEq%2FMGrxuqFs1UY8LS2Y5YkURYu643TJI75NKu1MSGSu%2Fput0lUf9clm%2FFHDVdTFj1u%2FTMMsnnZOnKGm%2FYPPJzN1Tvbg3H5lwVTO1efJJ2zILnbanLPT9wzkSRZ%2Bdvi%2FoxH%2BeipcSlf917z1%2FWBCR5nkBf89fvVZ%2BHd%2Fv%2FsL%2Fvzh5vJKls9jH5t6KVqSrMHNQbyyJf5rxn7ljedphkTWRUqx5cNcvAzFsZcyAa72I4itkzDYvd3Vt4yD6Pggj0kq0x1pLZOb8N7HkzKSOWvlkG7kJ2pzVvZ%2BVV1MPk2i8JZLH%2BfyiPO3%2FFU8FQeywVLs2qP8gN8Z9Gq%2BgDXV%2BeTq6qVi4zfb33SarB%2B48mCZ%2BJB7jLfiqc78svX3W2C743csq3qxh065bZiXEWcVezN1n1vwiN%2FqSL0E9FyHkerLaq6EE5yDE%2FniQh%2F5IGLqhhth7XYvgsXEYsl3yzYaTpNihPaKqIXRWdJlOSxj5OYN4Y%2FEMnyCxMznlUNyySMs2J4%2FFP5Tw7YmfXGP%2FHlsZ7JbXuzLf%2Flu4vsLInTTEjM8j64jPYdzyN%2BmiXLqtOI36r%2BRRXC%2FPdvSZYli2pjLwq8FgiqoDu%2BoZi7wJg72pjLl2YhiyYyPbJ4FpURKrIl20SoIYyNA1sbzO1RVqdlue9pumTTMJ5dlK%2BUA3yayEG%2FjYoMOA%2BDgMfq3C6JsxvPXBlx2Ut3QdMHqepsM0o%2F3RuLZD6KWSbPjlUcpI8ivz7O%2FWHwXjUMcmg6AmHddm8CjHXbAcnwXzUZl390RoZTA8MZu52S4RwcjMHrBkOEC1bE%2FQ%2F%2B0BUj9mBUF4B2y5f%2Fz0Oy7v6AlAyBlJCyPLiyHJqaTYyAMR%2BizAykLGtBHr9qGG5DkWY3MVtwUpja1G%2B9akRIYOq4aPAQXxEX1ykX%2F0pzaznPIfJnl1kEodK0ycTsrdS02%2FB6lta0oTamwgNZliC1WY8y1MhEikPESG4%2BhQjU0USKCOlNXbyhjiZSMNaCM08ipDefxIWszf7qzYEpb9OGmps2zlkp6c16lKH2JlIc%2BIKFEWlNXdQdqLWJFI9runyuRQPqbmJFIw7%2FXuWhqVKIxYJA8DQlxalHhhzO3ipOxzLlcDrghZo4p6WkOOtRBi%2FVxInDkqXpXSICEp3awIOXbOIkhCSnLt7gJZs4wfjA0jkPigHoNodg1JrkbvZXa%2FrG7gODupsOzknptySJOItJbKowQ%2B1NpDyE6Q0LFmFnQOATmy7U4URKCIlNHRhQfxMpGG%2FLvGEtRfg9jPiMF0s5I9aZk4FQdLpkcPZXdI6N3YgONTgVHsgyRSDPqSzsbq3Ni1edLtTiRArEVHA5vsENy0h3akMPNTmRMkK6UxdvqMmJFAx50IWzaRVZJExyDZp%2Fu0jxs1iS9tTjQIZnb7Wn65kyPF2o4eninKWS9tyNM9TxRArEahmQ9nyqWBbU80TKCGlPHRhQzxMpGGvtWd1BVCYTEqAweBrMT4QlUy8v3p6d71cz1VMXm2oSwa6B4A8HNek4sAaGpKMHtS1VYGnGYHLGYNfCbqxqqgf1JhUeyFI8rcatRxlqQyLFocvKqfXi111PE9zDswF1IpGyYbB2qt0pG0eYKEDNRqxoHKZ6aqfzyaPMCaD2JGnMw2tMY%2FVTPagHqfBAlh1IY9YrsEPtRqQ4ZGEWdVjPCpvM9KGmI1I8SGTqwGgwFF8TGJcRm5bmc5E%2F3putZ%2FXitaZPfmZ%2Ftaa5Aqo%2B1ND0cU5FSWzWoww1NJHiEPB0KsJluXCOJKcm9lBnEykkJDl18Yb6mkjBeMczFkZFjQEDiQSj6CSDs8ei01gVVR%2FqcPo4p6byBd0tsHzxmnMANTiR0rAU4ZQMTj0eUIMTKR6kNnVgQA1OpGBclnnDWnIh%2F4%2BL9yOpqaWF%2FM3%2BSk1z5VMHUH9zgHNKSlKzFmSovYmUhohlYbYKSG3qAw%2F1NpESQmpTF2%2Bot4kUDDmEM8GW83B6kt%2Fg1W0ewag3ydrssd40VkJ1ALU2BzgnpaQ3a4%2BmhlqbSGmIknhGgrMdEai9iRQREpw6MKD2JlIw6oKz60SCUHEOyeHsseI0Vj91CHU4hzgnprSCsx5lqMWJFIfkLubihm5Mbwk81OJESsh7ujFdG3GoyYkUjQm%2F5fKTT4tq%2FddX55OrN3kmsf5dZJVfSHzqgSC7s7%2Fi01wB1SHU7hzinKRSAdWdOI%2BgjidSIEwU78cmQEdQyxMpIyQ%2FdWBALU%2BkYBypeP%2BLF58jcj57LD5HppzPEdT5HOGcrZL43I0z1PtECoSJ6v3oxCfU%2FUTKCIlPXbyh3idSMI5Zvf%2FlK9AG%2BxNh9f7J%2BX8%2Fnv%2B5X%2Fl%2BV4nvlvL9jirxv6l7ZEw8Qp3LkX6uSXMGQ3MGY%2FX7x1B7UuGBLMnTYok6DlAnEikOtEyihQ2oGYmUDarfr0cD6jdiRYPq98M4ARuUpDHx1O8fQ11IhQey7EAasx5lqOGIFIdVSutx2wGBGo9IAaH1uPqIQ1dVIkVDux6XrTKphmhBbgsR5G%2F2V3uaq%2BdvW1CHc4xzbkrqc4cHqMWJlIdl%2FhgY0p%2BtiECdTqSIkABtYQNqdSJlo6ZAy4fXv%2BkumSDUnbZFpmePhaexmv62BbU914QgSxWkPHfCDDU%2BsQIhCaCFuC1Rh%2FqeWPkg1akNONT3xIrGhH8P%2BZ1sy1eE5kNAglOPADmd%2FRWc5ir72zbU6VwTgixJhN3lhZevNm2oz4mVBsGyDqcfCPWmDbU5sRJCelOLBtTlxIrGpLzV61bI93TyS0ZWlpysv7tJdzZCQ0Znj3WnsQr%2F62v3TycLG%2BfklOoOPAo02OpEigSVvYJQAjY8kVJCAlQbcLDhiRSNjeFJpa9%2BjhxyP3usQo1V%2FbcdsPtp45yykgp9hATYAkWKBNW%2FglACtkGRUkIqVIsG2AZFigbVwHoWPg2GKMIiWG8%2FnX%2F%2B%2BOXj%2BX5lsGz1XLdtseCMazDI02tY05FD1zOmI8FupqOfedIEYq%2B0MNaTYLoQlu2ALUt1DMhy%2FXOW6z4OnDvYP30%2F3dtBsjfYnUQKxL63dTwO3%2Fpr794EHOveD0oH2KBESse%2B5bCa4leDw%2FGH3dJxBDigHiRaOJ5fEOtxJG11CVuBoh621A0o9u4V8kOQ4oJdS1Kbh1ebQ2OzDBdsTSpCkGUIUps7YQa7kEiBiNm%2Bly5ehd50wVYkUj6uSW%2FqQw5deYkWjjj8e5UHRyaROMxyCLrMJyiVJ%2FmcPVae60tPBqQn2Oh0cU5OSXruhBlsdCIFIuDpVITLcpUdKVBd8MGOJ1JMSH9qAw72O5Gi0aA%2FN0mFVKieB6%2FB%2F0S4RKIolHZTLpT4uhcPTcskfLXQRXVjqa%2BZtYr0WtZgPU9GemAH09PPOWn%2B0FFuWKNgfJ2EemodIO76E%2Fkl5%2Fpupw%2FPWUD7dG8HSeFgZxIpEM%2BrqNug4FRbB2usW3o%2FKCNggxIpI%2FlqCTl21r6ldRtOda8uBsedziI87wiQgB1JpJB0WVu34cS36sS4bdpwj7xiHQMZsJdJIvTwItTc8gkPbFkqQpClChKhO2EGm5NIgaiMJ5KhrbEH%2B5RIKSEZ%2BjQkPnhJJlJIajJ0fXMXKdF2asgO7bESNbicwgf7oT7OWevz6k5gFKM%2B2BFFisRzq5%2B9CjHqgz1RpJSQBNUGHOyEIkXj91U8rYqeCVWCortCaK9EkVazEx7M%2BNbYNK%2B1SFZiytt6e4TZdCW%2B8%2FwAbCVO3wpRhPl8smBx8J8Cpm3VahcKzz3lcbDZ9QcXyZfkE4sfyr%2Fs7nsfZv%2FLUXszcqvNr9V7ys8gHsq%2F%2BWrzqyI0H1audHF57JlSuLrPqK5sb3GYF37On9cufyR3cT4fWuRHKscwv%2BaXNrMmeCRB%2FV4fdC1IcijYw9YOlfbe9HyZFM81UGiO7HopDL9KFht8yh47hmmICiY5hlqYPLsTmlR5wWaa7kSY8S2eRFHu8ShAeepJEc1APbm%2FbVUPWzdM4KhDAtWpfkQEnRYER0YRLHJX%2Bc3KJVX9oHCgLhYdmKoxLqpKcpqpcjuBau1faaiasy2gyqsS4XG%2BKW3rOJlKPVK0m%2B%2FKhruvDg2V36K8hkah2iyn%2FsajJJ7laBUP4ji6DLM99ficjuCSmyJJsu3dBVvOPyUBz%2Ff4Bw%3D%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E
