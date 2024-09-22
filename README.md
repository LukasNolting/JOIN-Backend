# Task Management API

This project is a Django-based API for managing tasks, subtasks, users, and contacts. It is designed to support features such as user authentication, task assignment, and contact management.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Authentication](#authentication)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher
- Django Rest Framework
- Postman (optional, for API testing)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LukasNolting/JOIN-Backend.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   - Run the migrations to create the necessary database tables:
     ```bash
     python manage.py migrate
     ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Running the Application

After starting the development server, the API will be available at `http://127.0.0.1:8000/`. You can test the endpoints using Postman or any other API client.

## API Endpoints

### User Authentication

- **Login:**
  - `POST /api/login/`
  - Request Body:
    ```json
    {
      "username": "user",
      "password": "password"
    }
    ```
  - Response:
    ```json
    {
      "token": "your-token",
      "user_id": 1,
      "email": "user@example.com",
      "initials": "AB",
      "color": "#FFFFFF",
      "rememberlogin": true,
      "username": "user",
      "first_name": "John",
      "last_name": "Doe",
      "name": "John Doe"
    }
    ```

### User Management

- **Create User:**
  - `POST /api/users/`
  - Request Body:
    ```json
    {
      "username": "user",
      "password": "password",
      "email": "user@example.com",
      "initials": "JD",
      "first_name": "John",
      "last_name": "Doe",
      "color": "#000000",
      "rememberlogin": false
    }
    ```
  - Response:
    ```json
    {
      "id": 1,
      "username": "user",
      "email": "user@example.com",
      "initials": "JD",
      "first_name": "John",
      "last_name": "Doe",
      "color": "#000000",
      "rememberlogin": false
    }
    ```

- **Get All Users:**
  - `GET /api/users/`
  - Response: List of all users.

### Task Management

- **Get All Tasks:**
  - `GET /api/tasks/`
  - Response: List of all tasks.

- **Get Task by ID:**
  - `GET /api/tasks/<id>/`
  - Response: Task details.

- **Create Task:**
  - `POST /api/tasks/`
  - Request Body:
    ```json
    {
      "title": "New Task",
      "category": "Work",
      "categoryboard": "Board 1",
      "assignedTo": ["User 1", "User 2"],
      "assignedToID": [1, 2],
      "colors": ["#FF0000", "#00FF00"],
      "description": "Task description",
      "dueDate": "2023-12-31",
      "prio": "High",
      "subtasks": [
        {"title": "Subtask 1", "subtaskStatus": false}
      ]
    }
    ```

- **Update Task:**
  - `PUT /api/tasks/<id>/`
  - Request Body: Same as for task creation.

- **Delete Task:**
  - `DELETE /api/tasks/<id>/`

### Contact Management

- **Get All Contacts:**
  - `GET /api/contacts/`
  - Response: List of all contacts.

- **Create Contact:**
  - `POST /api/contacts/`
  - Request Body:
    ```json
    {
      "firstname": "John",
      "lastname": "Doe",
      "fullname": "John Doe",
      "initials": "JD",
      "email": "john.doe@example.com",
      "phone": "123456789",
      "color": "#000000",
      "taskassigned": true,
      "contactAssignedTo": 1
    }
    ```

- **Update Contact:**
  - `PUT /api/contacts/<id>/`
  - Request Body: Same as for contact creation.

- **Delete Contact:**
  - `DELETE /api/contacts/<id>/`

## Models

- **TaskItem**: Represents a task with fields like title, description, category, due date, priority, and relationships to users and subtasks.
- **Subtask**: Represents a subtask linked to a `TaskItem`.
- **CustomUser**: Extends Django's `AbstractUser` with additional fields like initials, color, and remember login.
- **Contacts**: Stores information about contacts and their relationships to `CustomUser`.

## Authentication

This project uses token-based authentication. To access protected endpoints, include the token in the `Authorization` header as follows:

```
Authorization: Token your-token
```

## Contributing

Contributions are welcome! Please create an issue first to discuss what you would like to change. You can also fork the repository, make changes, and submit a pull request.
