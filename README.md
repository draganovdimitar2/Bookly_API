# Bookly

**Description**: Bookly is a web-based application designed for managing book records. Users can perform CRUD (Create, Read, Update, Delete) operations on books within a centralized database. The goal of the project is to build a robust and scalable book management REST API using FastAPI, incorporating essential web application features such as authentication, authorization, background tasks, email notifications, and more.

This project is complete and deployed on Render. You can access the live API documentation at https://bookly-api-ymlo.onrender.com/api/v1/docs.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Setup](#project-setup)
3. [Running the Application](#running-the-application)


## Getting Started
Follow the instructions below to set up and run your FastAPI project.

### Prerequisites
Ensure you have the following installed:

- Python >= 3.10
- PostgreSQL

## Project Setup
1. Clone the project repository:
    ```bash
    git clone https://github.com/draganovdimitar2/Bookly_API.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd Bookly
    ```

3. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Run database migrations to initialize the database schema:
    ```bash
    alembic upgrade head
    ```

## Running the application
Start the application:
```bash
fastapi dev src/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.





