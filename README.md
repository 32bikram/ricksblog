# Rick's Blog[🔗](https://ricksblogfrontend-14d2.vercel.app)
A blog API built with FastAPI, PostgreSQL, and SQLAlchemy. You can sign up, log in with a JWT, write posts, delete your posts, and like/unlike other people's posts.
The fun part: whatever you write gets run through Gemini before it's saved, and comes back rewritten in Rick Sanchez's voice — same meaning, same facts, just filtered through Rick's particular way of putting things.

## Features

- User accounts with hashed passwords
- JWT login via OAuth2 password flow
- Full CRUD on posts, scoped so you can only delete your own
- Post discovery — list everything (with search + limit), pull a specific user's posts, or just your own
- Like/unlike posts, with vote counts returned alongside each post
- Every post gets rewritten in Rick's voice before it's stored
- Alembic migrations for schema versioning
- Docker Containerization for easier deployment

## Tech Stack

| Layer             | Technology                                 |
|--------------------|--------------------------------------------|
| Framework          | FastAPI                                    |
| Database           | PostgreSQL                                 |
| ORM                | SQLAlchemy 1.4                             |
| Migrations         | Alembic                                    |
| Auth               | OAuth2 (password flow) + JWT (python-jose) |
| Password hashing   | passlib / pwdlib (bcrypt)                  |
| Validation         | Pydantic                                   |
| Server             | Uvicorn / Gunicorn                         |
| Post rewriting     | Google Gemini (google-genai)               |

## Project Structure

```
ricksblog-main/
├── application/
│   ├── main.py          # FastAPI app instance, CORS, router registration
│   ├── config.py         # Environment-based settings (Pydantic)
│   ├── database.py        # SQLAlchemy engine, session, and Base
│   ├── models.py           # ORM models: Post, Users, Votes
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── oauth2.py             # JWT creation/verification, current-user dependency
│   ├── utils.py                # Password hashing helpers
│   ├── makethepost.py           # Calls Gemini to rewrite post content as Rick
│   └── routers/
│       ├── auth.py               # /login
│       ├── user.py                # /createuser, /getuser/{id}
│       ├── post.py                 # /posts (CRUD + search + per-user listing)
│       └── votes.py                 # /votes (like/unlike)
├── alembic/                # Database migration scripts
├── alembic.ini
├── docker-compose-dev.yml
├── docker-compose-prod.yml
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
- A Gemini API key (for the Rick-ification of posts)

### Installation

1. Clone the repo and move into it:
   ```bash
   git clone <repo-url>
   cd ricksblog-main
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

4. Create a `.env` file in the project root:
   ```env
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_USERNAME=your_db_user
   DATABASE_PASSWORD=your_db_password
   DATABASE_NAME=ricksblog
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   LLM_API=your_gemini_api_key
   ```

5. Run migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the server:
   ```bash
   uvicorn application.main:app --reload
   ```

The API runs at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## API Overview

| Method | Endpoint                  | Description                                            | Auth required |
|--------|-----------------------------|----------------------------------------------------------|:--------------:|
| POST   | `/createuser`                 | Register a new user                                        | No             |
| GET    | `/getuser/{id}`                | Get a user by ID                                            | No             |
| POST   | `/login`                        | Log in, get a JWT access token                                | No             |
| GET    | `/posts/`                        | List all posts (supports `search`, `limit`)                     | Yes            |
| GET    | `/posts/{username}`               | List posts by a specific user                                     | Yes            |
| GET    | `/posts/myposts/myposts`           | List your own posts                                                  | Yes            |
| POST   | `/posts/`                            | Create a post (gets rewritten in Rick's voice first)                   | Yes            |
| DELETE | `/posts/{id}`                          | Delete a post you own                                                     | Yes            |
| POST   | `/votes`                                 | Like (`dir=1`) or unlike (`dir=0`) a post                                   | Yes            |

Protected routes need an `Authorization: Bearer <token>` header, using the token you get back from `/login`.

## Docker

The backend image is published on Docker Hub as [`kiertolainen/ricksblog`](https://hub.docker.com/r/kiertolainen/ricksblog).

Two Compose files are included:

- `docker-compose-dev.yml` — dev setup, builds from source
- `docker-compose-prod.yml` — pulls the published image, runs with Gunicorn + Uvicorn workers

Make sure your `.env` is in the project root (needed for the prod file), then:

```bash
# Development
docker compose -f docker-compose-dev.yml up -d

# Production
docker compose -f docker-compose-prod.yml up -d
```

To pull the image directly instead of building from source:

```bash
docker pull kiertolainen/ricksblog:latest
```

---

The frontend at the site on the link above is generated by an LLM for displaying the api.
