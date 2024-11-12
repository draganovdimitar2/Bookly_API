# Bookly

**Description**: Bookly is a project where you can add, delete, update, and view book records. The goal is to build a robust book management REST API using FastAPI, integrating various essential features commonly needed in web applications.

This project is currently in progress, and I’ll be implementing it step-by-step, covering everything from initial setup to deployment.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Redis Setup](#redis-setup)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)


## Getting Started
Follow the instructions below to set up and run your FastAPI project.

### Prerequisites
Ensure you have the following installed:

- Python >= 3.10
- PostgreSQL
- Redis

## Redis Setup

### Using WSL
Install Redis in a WSL environment (Linux on Windows).

### Starting Redis

To start Redis, use the following commands based on your operating system:

- **Linux/MacOS**:
    ```bash
    redis-server
    ```

- **Windows (via WSL)**:
    ```bash
    redis-server
    ```

### Redis Configuration

Ensure that your `.env` file contains the correct Redis configuration. Update the `.env` file with these settings:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
```
This configuration ensures that your application will be able to connect to Redis for caching and background tasks.

### Example of .env File
Here’s an example of what your .env file might look like:
```env
DATABASE_URL = postgresql+asyncpg://postgres:your_password@localhost:5432/booklydb
JWT_SECRET = your_jwt_secret_key
JWT_ALGORITHM = HS256
REDIS_HOST = localhost
REDIS_PORT = 6379
```

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

5. Set up environment variables by copying the example configuration:
    ```bash
    cp .env.example .env
    ```

6. Run database migrations to initialize the database schema:
    ```bash
    alembic upgrade head
    ```

7. Open a new terminal and ensure your virtual environment is active. Start the Celery worker (Linux/Unix shell):
    ```bash
    sh runworker.sh
    ```

## Running the application
Start the application:
```bash
fastapi dev src/
```
Alternatively, you can run the application using Docker:
```bash
docker compose up -d
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.





