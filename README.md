📘 Term Model Service

A FastAPI-based REST service that manages multilingual business terms, their selfsame meanings, and synonyms, backed by PostgreSQL, containerized using Docker, and designed for cloud deployment (Google Cloud Run).


![alt text](<solution architecture image format.png>)



🚀 Project Overview

The Term Model Service is a semantic dictionary system that helps organizations:

Manage standardized business terms

Link terms across languages and regions

Group terms that mean exactly the same concept

Handle synonyms used interchangeably in reports or systems

This project was built as part of an intern orientation / backend system design exercise.

🧠 Core Concepts
1️⃣ Term

Represents a single business term in a specific language and country.

2️⃣ TermSelfsame

Groups multiple terms that represent the same concept across languages.

3️⃣ TermSynonym

Groups different words that are treated as equivalent in usage.

🗂️ Project Structure
term-model-service/
│
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── db.py                   # Database connection & session management
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── security.py             # JWT, password hashing, token handling
│   ├── dependencies.py         # Auth dependencies (get_current_user)
│   │
│   └── routers/
│       ├── auth.py             # Authentication routes (register, login)
│       ├── terms.py            # CRUD for Term
│       ├── term_selfsame.py    # CRUD for TermSelfsame
│       └── term_synonym.py     # CRUD for TermSynonym
│
├── schema.sql                  # PostgreSQL schema definition
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Local multi-container setup
├── README.md                   # Project documentation
└── .env                        # Environment variables (not committed)

🛠️ Tech Stack

Backend Framework: FastAPI

Database: PostgreSQL

ORM: SQLAlchemy

Authentication: JWT (OAuth2 Password Flow)

Containerization: Docker & Docker Compose

Cloud Platform: Google Cloud Run
<<<<<<< HEAD

API Docs: Swagger UI (/docs)

🔐 Authentication Flow

User registers via /auth/register

User logs in via /auth/login

JWT access token is returned

Token is passed as:

Authorization: Bearer <token>


Protected endpoints require a valid token

📦 Database Schema
Term
Column	Description
term_rid	Primary key
turf_rid	Domain identifier
term_id	Business identifier
language	Language code
country	Country code
term_name	Display name
term_description	Explanation
term_acronym	Short form
is_machinized_name	Boolean
is_standardized_name	Boolean
TermSelfsame

Links terms that mean the same concept.

TermSynonym

Links different words used interchangeably.

❗ Cascade delete is intentionally disabled to prevent accidental data loss.

🔄 CRUD API Endpoints
🔑 Auth

POST /auth/register

POST /auth/login

📘 Term

GET /terms/

POST /terms/

GET /terms/{term_rid}

PUT /terms/{term_rid}

DELETE /terms/{term_rid}

🔗 TermSelfsame

GET /term-selfsame/

POST /term-selfsame/

DELETE /term-selfsame/{term_selfsame_rid}

🔁 TermSynonym

GET /term-synonym/

POST /term-synonym/

DELETE /term-synonym/{term_synonym_rid}

🧪 Running Locally
1️⃣ Clone Repository
git clone https://github.com/<your-username>/term-model-service.git
cd term-model-service

2️⃣ Start with Docker
docker-compose up --build

3️⃣ Access API

Swagger UI → http://localhost:8000/docs

Health check → http://localhost:8000/health

☁️ Cloud Deployment (Google Cloud Run)

High-level steps:

Enable billing on GCP project

Enable required services:

Cloud Run

Cloud Build

Artifact Registry

Build & push Docker image

Deploy to Cloud Run

Configure environment variables

Cloud Run provides auto-scaling and HTTPS by default.

🏗️ Architecture Overview
High-Level Design

Client → FastAPI → PostgreSQL

JWT-based authentication

Stateless API suitable for cloud deployment

Low-Level Design

SQLAlchemy ORM models

Dependency-based auth validation

Modular routers per entity

✅ Key Design Decisions

Stateless JWT auth (cloud-friendly)

Explicit relationship tables

No cascade delete for safety

Clean separation of concerns

Swagger-first API validation

📌 Future Enhancements

Role-based access control (RBAC)

Soft deletes

Audit logging

Search & filtering

Admin dashboard

👤 Author

Tarunesh R

                   
                   
=======

API Docs: Swagger UI (/docs)

🔐 Authentication Flow

User registers via /auth/register

User logs in via /auth/login

JWT access token is returned

Token is passed as:

Authorization: Bearer <token>


Protected endpoints require a valid token

📦 Database Schema
Term
Column	Description
term_rid	Primary key
turf_rid	Domain identifier
term_id	Business identifier
language	Language code
country	Country code
term_name	Display name
term_description	Explanation
term_acronym	Short form
is_machinized_name	Boolean
is_standardized_name	Boolean
TermSelfsame

Links terms that mean the same concept.

TermSynonym

Links different words used interchangeably.

❗ Cascade delete is intentionally disabled to prevent accidental data loss.

🔄 CRUD API Endpoints
🔑 Auth

POST /auth/register

POST /auth/login

📘 Term

GET /terms/

POST /terms/

GET /terms/{term_rid}

PUT /terms/{term_rid}

DELETE /terms/{term_rid}

🔗 TermSelfsame

GET /term-selfsame/

POST /term-selfsame/

DELETE /term-selfsame/{term_selfsame_rid}

🔁 TermSynonym

GET /term-synonym/

POST /term-synonym/

DELETE /term-synonym/{term_synonym_rid}

🧪 Running Locally
1️⃣ Clone Repository
git clone https://github.com/<your-username>/term-model-service.git
cd term-model-service

2️⃣ Start with Docker
docker-compose up --build

3️⃣ Access API

Swagger UI → http://localhost:8000/docs

Health check → http://localhost:8000/health

☁️ Cloud Deployment (Google Cloud Run)

High-level steps:

Enable billing on GCP project

Enable required services:

Cloud Run

Cloud Build

Artifact Registry

Build & push Docker image

Deploy to Cloud Run

Configure environment variables

Cloud Run provides auto-scaling and HTTPS by default.

🏗️ Architecture Overview
High-Level Design

Client → FastAPI → PostgreSQL

JWT-based authentication

Stateless API suitable for cloud deployment

Low-Level Design

SQLAlchemy ORM models

Dependency-based auth validation

Modular routers per entity

✅ Key Design Decisions

Stateless JWT auth (cloud-friendly)

Explicit relationship tables

No cascade delete for safety

Clean separation of concerns

Swagger-first API validation

📌 Future Enhancements

Role-based access control (RBAC)

Soft deletes

Audit logging

Search & filtering

Admin dashboard

👤 Author

Tarunesh R
>>>>>>> 14818f628effcefd9a4a0171ea984e63990ecec0
