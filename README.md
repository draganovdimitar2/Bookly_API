
# Bookly

**Description:**
Bookly is a project where you can add, delete, update, and view book records. The goal is to build a robust book management REST API using FastAPI, integrating various essential features commonly needed in web applications.

This project is currently in progress, and I’ll be implementing it step-by-step, covering everything from initial setup to deployment.

## Project outline

1. Project setup
   - Setting up FastAPI, creating a basic web server, and running it with FastAPI CLI.

2. API endpoints
   - Implementing CRUD operations for managing book records.
   - Using path and query parameters, request bodies, and handling headers.

3. Database integration
   - Setting up a database with SQLModel.
   - Organizing and managing API paths with routers.
   - Implementing CRUD with SQLModel and using service classes.

4. User Authentication
   - Setting up user accounts, password hashing, and JWT authentication.
   - Enabling refresh tokens, session management, and access control based on user roles.

5. Error handling and middleware
   - Implementing custom error handling and creating middleware for logging and CORS.

6. Additional features
   - Email support for verification and password resets.
   - Background tasks with Celery and Redis.
   - Thorough API documentation with SwaggerUI and Redoc.
   - Unit testing and deployment on Render.com.

## Installation

To set up the project locally:

1. Clone the repository:
git clone https://github.com/YOUR_USERNAME/Bookly.git cd Bookly

2. Install dependencies:
pip install -r requirements.txt

3. Run the FastAPI server:
uvicorn main--reload

## Usage

- Visit `http://127.0.0.1:8000/docs` to access the interactive API documentation with SwaggerUI.
- Use the endpoints to add, delete, update, and view book records.
