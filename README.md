# Hotel Appointment Management System

This project is a backend system for managing appointment scheduling, cancellations, and rescheduling for a hotel. It uses Flask, SQLAlchemy, and SQLite to provide a RESTful API for handling appointments.

## Features

- **Appointment Scheduling**: Book new appointments specifying the date.
- **Appointment Cancellation**: Cancel existing appointments.
- **Appointment Rescheduling**: Reschedule existing appointments.
- **Date Range Filtering**: Check for appointment conflicts within a specified date range.

## Technologies

- **Flask**: For creating the API endpoints.
- **Flask-RESTful**: An extension for building REST APIs with Flask.
- **SQLAlchemy**: ORM for database interactions.
- **SQLite**: Lightweight database for easy setup.
- **Marshmallow**: For schema validation and serialization.

## Setup

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/jaysinscars/room-appointment-scheduler.git
    cd room-appointment-scheduler
    ```

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:

    ```bash
    flask db upgrade
    ```

5. **Run the application**:

    ```bash
    flask run
    ```

    By default, the application will run on `http://127.0.0.1:5000/`.

## API Endpoints

### Book an Appointment

- **URL**: `/appointments`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "room_id": "1",
        "phone": "123-456-7890",
        "email": "example@example.com",
        "name": "John Doe",
        "appointment_time": "2024-08-21"
    }
    ```
- **Response**: Confirmation of appointment creation or an error message if the slot is not available.

### Cancel an Appointment

- **URL**: `/appointments/{id}/cancel`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "customer_id": "1"
    }
    ```
- **URL Parameters**:
    - `id`: ID of the appointment to be canceled.
- **Response**: Confirmation of appointment cancellation.

### Reschedule an Appointment

- **URL**: `/appointments/{id}/reschedule`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "customer_id": "1",
        "appointment_time": "2024-08-22T00:00:00",
        "room_id": "1"
    }
    ```
- **URL Parameters**:
    - `id`: ID of the appointment to be rescheduled.
- **Response**: Confirmation of appointment rescheduling or an error message if the new slot is not available.

## Configuration

You can configure environment-specific settings using environment variables. The default environment file is `.env`. Set the `CURRENT_ENV` variable to specify a different environment file if needed.


## Deployment

You can deploy this application on cloud platforms like AWS, Heroku, or Azure. Refer to the respective platform’s documentation for deployment instructions.

---
