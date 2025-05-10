# Bookly

**Description**: Bookly is a web-based application designed for managing book records. Users can perform CRUD (Create, Read, Update, Delete) operations on books within a centralized database. The goal of the project is to build a robust and scalable book management REST API using FastAPI, incorporating essential web application features such as authentication, authorization, background tasks, email notifications, and a real-time notification system.

This project is complete and deployed on Render. You can access the live API documentation at https://bookly-api-ymlo.onrender.com/api/v1/docs.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Setup](#project-setup)
3. [Running the Application](#running-the-application)


## Getting Started
### Prerequisites
- Azure account with Service Bus instance
- Python >= 3.10
- PostgreSQL
  
### Azure Service Bus Integration

In the latest update, Bookly includes a notification system that alerts all users when a new review is submitted for any book.

Here’s how the notification flow works:

1. ✅ Review Submission →
2. ✅ Review Stored in PostgreSQL Database →
3. ✅ Message Sent to Azure Service Bus Queue →
4. ✅ Webhook Triggered Using Message Data →
5. ✅ Webhook Notifies All Users About the New Review →
6. ✅ Message Deleted from Queue

This system ensures that all users stay informed in real time when new reviews are added.

### Steps to Set Up:
1. You must set up an **Azure Service Bus** instance.
2. Ensure that you have a **connection string** and a **queue name** configured for the service bus.
3. Once your **Azure Service Bus** instance is ready, update your `.env` file with the corresponding values for `AZURE_SERVICE_BUS_CONNECTION_STRING` and `AZURE_SERVICE_BUS_QUEUE_NAME`.

### Environment Variables

Make sure to include the following variables in your `.env` file to run the project correctly. Below is an example `.env` configuration:
```bash
DATABASE_URL=postgresql+asyncpg://your_db_user:your_db_password@your_db_host/your_db_name
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
SENDGRID_API_KEY=your_sendgrid_api_key  # API key used to send emails
MAIL_FROM=bookly.application.email@abv.bg  # This is an actual test email (hope it won't be compromised soon)
MAIL_FROM_NAME=Bookly
DOMAIN=https://bookly-api-ymlo.onrender.com

# Azure Service Bus Configuration
AZURE_SERVICE_BUS_CONNECTION_STRING=your_azure_bus_connection_string
AZURE_SERVICE_BUS_QUEUE_NAME=your_azure_service_bus_queue_name

# Webhook URL for notifications
WEBHOOK_URL=https://webhook.site/38ec8555-ebc3-4a32-94f9-9432a3cf5b82  # Using webhook.site for demo purposes (you can replace it with your own URL)

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
    python3 -m venv .venv
    ```
    * for powershell
    ```bash
    .venv\Scripts\activate
    ```
    * for linux/os
    ```bash
    source .venv/bin/activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt "fastapi[standard]"
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





