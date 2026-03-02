
# User CRUD with Profile — FastAPI + SQLAlchemy

Tech documentation for a **CRUD system** that manages **Users** and **Profiles** using **Python + FastAPI + SQLAlchemy ORM**.

This project satisfies the practical requirements:

- **Entities:** User + Profile  
- **Relationship:** **1:1 (User → Profile)**  
- **CRUD:** Full CRUD for **User** (and **Profile** routes included)  
- **Create flow:** When creating a user, allow **creating the profile together**  
- **Email uniqueness:** Do **not** allow duplicate emails  
- **Listing:** List users including **profile data** using SQLAlchemy relationships  

---

## 1. Tech Stack

- **Language:** Python `X.Y.Z`
- **Framework:** FastAPI `X.Y.Z`
- **ORM:** SQLAlchemy `X.Y.Z`
- **Migrations:** Alembic `X.Y.Z` (recommended)
- **Database:** SQLite (dev) or PostgreSQL/MySQL (optional)

> Replace versions after installation:
```bash
python --version
pip show fastapi sqlalchemy alembic
```

---

## 2. Project Setup

### 2.1 Clone repository

```bash
git clone <YOUR_REPO_URL>
cd <YOUR_REPO_FOLDER>
```

### 2.2 Create and activate virtual environment

Create:

```bash
python -m venv .venv
```

Activate:

* Windows:

```bash
.venv\Scripts\activate
```

* Linux/Mac:

```bash
source .venv/bin/activate
```

### 2.3 Install dependencies

```bash
pip install -r requirements.txt
```

### 2.4 Environment configuration

Create a `.env` file in the project root.

**Option A — SQLite (recommended for class/demo):**

```env
DATABASE_URL=sqlite:///./app.db
```

**Option B — PostgreSQL example:**

```env
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/crud_users
```

### 2.5 Run migrations (Alembic)

If you use Alembic (recommended):

```bash
alembic upgrade head
```

### 2.6 Run the API

```bash
uvicorn app.main:app --reload
```

Default URL:

* `http://127.0.0.1:8000`

Docs:

* Swagger: `http://127.0.0.1:8000/docs`
* Redoc: `http://127.0.0.1:8000/redoc`

---

## 3. Project Structure

Suggested structure aligned with a simple modular backend (routes / controllers / services style):

```txt
app/
  main.py

  core/
    config.py
    security.py

  db/
    session.py
    base.py

  models/
    user.py
    profile.py

  schemas/
    user.py
    profile.py

  services/
    users_service.py
    profiles_service.py

  api/
    routes/
      users.py
      profiles.py

  middlewares/
    error_handler.py

alembic/
  versions/

requirements.txt
.env
```

### Responsibilities

* **models/**: SQLAlchemy models and relationships
* **schemas/**: Pydantic request/response schemas
* **services/**: business logic + SQLAlchemy queries
* **routes/**: API endpoints (FastAPI routers)
* **db/**: session management and base model
* **core/security.py**: password hashing helpers

---

## 4. Expected Database Modeling

### 4.1 Entities

#### User

* `id`
* `name`
* `email`
* `password`
* `profile_id`

#### Profile

* `id`
* `profile_name`

### 4.2 Constraints (Mandatory)

* `users.email` must be **unique**
* Relationship must be **1:1** (one user → one profile)

### 4.3 Relational Modeling (Recommended)

To enforce true **1:1**, use:

* `users.profile_id` as **Foreign Key** to `profiles.id`
* `users.profile_id` as **UNIQUE**
* `users.email` as **UNIQUE**

Suggested table constraints:

#### `profiles`

| Column       | Type         | Constraints |
| ------------ | ------------ | ----------- |
| id           | integer/uuid | PK          |
| profile_name | varchar      | NOT NULL    |

#### `users`

| Column     | Type         | Constraints                            |
| ---------- | ------------ | -------------------------------------- |
| id         | integer/uuid | PK                                     |
| name       | varchar      | NOT NULL                               |
| email      | varchar      | NOT NULL, **UNIQUE**                   |
| password   | varchar      | NOT NULL (hashed)                      |
| profile_id | integer/uuid | NOT NULL, **UNIQUE**, FK → profiles.id |

---

## 5. API Routes

Base URL:

* `http://127.0.0.1:8000`

### 5.1 Users (Required CRUD)

| Method | Route         | Description                                    |
| ------ | ------------- | ---------------------------------------------- |
| POST   | `/users`      | Create user (allows profile creation together) |
| GET    | `/users`      | List users (must include profile)              |
| GET    | `/users/{id}` | Get user details (include profile)             |
| PUT    | `/users/{id}` | Update user (optional profile update)          |
| DELETE | `/users/{id}` | Delete user                                    |

### 5.2 Profiles (Included CRUD)

| Method | Route            | Description                                   |
| ------ | ---------------- | --------------------------------------------- |
| POST   | `/profiles`      | Create profile                                |
| GET    | `/profiles`      | List profiles                                 |
| GET    | `/profiles/{id}` | Get profile details (optionally include user) |
| PUT    | `/profiles/{id}` | Update profile                                |
| DELETE | `/profiles/{id}` | Delete profile                                |

---

## 6. Request/Response Examples

### 6.1 Create User with Profile (Required)

**POST** `/users`

Request:

```json
{
  "name": "John Doe",
  "email": "john@email.com",
  "password": "123456",
  "profile": {
    "profile_name": "admin"
  }
}
```

Expected response (example):

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@email.com",
  "profile": {
    "id": 1,
    "profile_name": "admin"
  }
}
```

Implementation notes:

* Create `Profile` first, then create `User` with `profile_id`
* Hash password before saving
* Reject duplicate emails using DB constraint + exception handling

---

### 6.2 Duplicate Email Error (Required)

If a user tries to register using an email that already exists, the API must reject it.

Suggested error response:

```json
{
  "message": "Email already in use",
  "code": "EMAIL_DUPLICATE"
}
```

In SQLAlchemy this usually happens as an `IntegrityError` (unique constraint violation).

---

### 6.3 List Users with Profile (Required)

**GET** `/users`

Expected response:

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@email.com",
    "profile": {
      "id": 1,
      "profile_name": "admin"
    }
  }
]
```

Implementation notes:

* Use relationship loading (e.g., `joinedload(User.profile)` or proper eager loading)
* Ensure responses return nested profile data

---

### 6.4 Get User by ID with Profile

**GET** `/users/{id}`

Example:
**GET** `/users/1`

Response:

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@email.com",
  "profile": {
    "id": 1,
    "profile_name": "admin"
  }
}
```

---

### 6.5 Update User (Optional profile update)

**PUT** `/users/{id}`

Request:

```json
{
  "name": "John Updated",
  "profile": {
    "profile_name": "manager"
  }
}
```

Response:

```json
{
  "id": 1,
  "name": "John Updated",
  "email": "john@email.com",
  "profile": {
    "id": 1,
    "profile_name": "manager"
  }
}
```

---

### 6.6 Delete User

**DELETE** `/users/{id}`

Response example:

```json
{
  "message": "User deleted successfully"
}
```

---

### 6.7 Create Profile (Profiles CRUD)

**POST** `/profiles`

Request:

```json
{
  "profile_name": "admin"
}
```

Response:

```json
{
  "id": 1,
  "profile_name": "admin"
}
```

---

### 6.8 List Profiles

**GET** `/profiles`

Response:

```json
[
  {
    "id": 1,
    "profile_name": "admin"
  }
]
```

---

## 7. Quick Testing (cURL)

### Create user with profile

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@email.com","password":"123456","profile":{"profile_name":"admin"}}'
```

### List users

```bash
curl http://127.0.0.1:8000/users
```

### Create profile

```bash
curl -X POST http://127.0.0.1:8000/profiles \
  -H "Content-Type: application/json" \
  -d '{"profile_name":"admin"}'
```

---

## 8. Delivery Checklist

* [ ] README includes: setup steps, dependencies, language version, ORM version
* [ ] User CRUD complete
* [ ] Profile CRUD included
* [ ] Create user with profile in same request
* [ ] Unique email enforced (DB unique + `IntegrityError` handling)
* [ ] List users includes profile data (SQLAlchemy relationship)

```
```
