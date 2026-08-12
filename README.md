# Rick's Blog

A RESTful blog API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. Users can create accounts, log in with JWT-based authentication, publish and manage(Update, Delete) posts, and like/unlike other users' posts.

## Features

- **User accounts** — registration with hashed passwords, and lookup by user ID
- **JWT authentication** — OAuth2 password-flow login that issues a bearer token for protected routes
- **Posts (CRUD)** — create, read, update, and delete blog posts, scoped to the logged-in owner
- **Post discovery** — list all posts (with title search and result limit), fetch posts by username, or fetch your own posts
- **Voting** — like/unlike posts, with vote counts returned alongside each post
- **Database migrations** — schema versioning via Alembic

## Tech Stack

| Layer          | Technology                                 |
|----------------|--------------------------------------------|
| Framework      | FastAPI                                    |
| Database       | PostgreSQL                                 |
| ORM            | SQLAlchemy 1.4                             |
| Migrations     | Alembic                                    |
| Auth           | OAuth2 (password flow) + JWT (python-jose) |
| Password hashing | passlib / pwdlib (bcrypt)                |
| Validation     | Pydantic                                   |
| Server         | Uvicorn                                    |
_______________________________________________________________
## Project Structure

```
ricksblog-master/
├── application/
│   ├── main.py         # FastAPI app instance, CORS, router registration
│   ├── config.py        # Environment-based settings (Pydantic)
│   ├── database.py       # SQLAlchemy engine, session, and Base
│   ├── models.py         # ORM models: Post, Users, Votes
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── oauth2.py          # JWT creation/verification, current-user dependency
│   ├── utils.py           # Password hashing helpers
│   └── routers/
│       ├── auth.py         # /login
│       ├── user.py         # /createuser, /getuser/{id}
│       ├── post.py         # /posts (CRUD + search + per-user listing)
│       └── votes.py        # /votes (like/unlike)
├── alembic/               # Database migration scripts
├── alembic.ini
└── requirements.txt
```

## Data Model

- **Users** — `id`, `email`, `username`, `password` (hashed), `created_at`
- **Posts** — `id`, `title`, `content`, `published`, `created_at`, `owner_id` (FK → Users)
- **Votes** — `user_id` (FK → Users) + `posts_id` (FK → Posts), composite primary key

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL running locally or accessible remotely

### Installation

1. Clone the repository and move into it:
   ```bash
   git clone <repo-url>
   cd ricksblog-master
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your database and JWT settings:
   ```env
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_USERNAME=your_db_user
   DATABASE_PASSWORD=your_db_password
   DATABASE_NAME=ricksblog
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the server:
   ```bash
   uvicorn application.main:app --reload
   ```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## API Overview

| Method | Endpoint                     | Description                              | Auth required |
|--------|-------------------------------|-------------------------------------------|:--------------:|
| POST   | `/createuser`                  | Register a new user                       | No             |
| GET    | `/getuser/{id}`                | Get a user by ID                          | No             |
| POST   | `/login`                       | Log in and receive a JWT access token     | No             |
| GET    | `/posts/`                      | List all posts (supports `search`, `limit`) | Yes         |
| GET    | `/posts/{username}`             | List posts by a specific user             | Yes             |
| GET    | `/posts/myposts/myposts`        | List the current user's own posts         | Yes             |
| POST   | `/posts/`                       | Create a new post                          | Yes             |
| PUT    | `/posts/{id}`                    | Update a post you own                     | Yes             |
| DELETE | `/posts/{id}`                    | Delete a post you own                     | Yes             |
| POST   | `/votes`                        | Like (`dir=1`) or unlike (`dir=0`) a post | Yes             |

Protected routes require an `Authorization: Bearer <token>` header, using the token returned from `/login`.
