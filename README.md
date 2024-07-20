# Django Backend Project

## Overview

This project is a Django-based backend application that provides user authentication and post management functionalities. It includes features like user signup, login, and logout, as well as creating, fetching, and liking posts. The project uses Django REST Framework to build the API endpoints and SQLite as the database.

## Tech Stack

- **Backend Framework**: Django, Django REST Framework
- **Database**: SQLite
- **Authentication**: JWT (JSON Web Tokens)
- **Deployment**: AWS EC2
- **Environment Management**: Virtualenv

## Features

1. **User Authentication**:
   - Signup
   - Login
   - Logout
2. **Post Management**:
   - Create posts
   - Fetch posts
   - Like posts

## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/backend-project.git
    cd backend-project
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv backend
    source backend/bin/activate
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### User Authentication

- **Signup**: `POST /api/signup/`
- **Login**: `POST /api/login/`
- **Logout**: `POST /api/logout/`

### Post Management

- **Fetch Posts**: `GET /api/posts/`
- **Create Post**: `POST /api/posts/`
- **Like Post**: `POST /api/posts/<post_id>/like_post/`

## Deployment to AWS

1. **Launch an EC2 instance**:
   - Choose an Amazon Machine Image (AMI) with Ubuntu.
   - Select an instance type (e.g., t2.micro).
   - Configure security groups to allow HTTP and SSH access.

2. **Connect to your EC2 instance**:
    ```bash
    ssh -i your-key.pem ubuntu@your-ec2-public-ip
    ```

3. **Install necessary software**:
    ```bash
    sudo apt update
    sudo apt install python3-pip python3-venv nginx
    ```

4. **Clone the repository on the EC2 instance**:
    ```bash
    git clone https://github.com/yourusername/backend-project.git
    cd backend-project
    ```

5. **Setup the virtual environment and install dependencies**:
    ```bash
    python3 -m venv backend
    source backend/bin/activate
    pip install -r requirements.txt
    ```

6. **Run migrations and create a superuser**:
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

7. **Configure Gunicorn**:
    ```bash
    pip install gunicorn
    gunicorn --bind 0.0.0.0:8000 your_project_name.wsgi:application
    ```

8. **Setup Nginx**:
    ```bash
    sudo nano /etc/nginx/sites-available/backend_project
    ```
    Add the following configuration:
    ```
    server {
        listen 80;
        server_name your-ec2-public-ip;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

9. **Enable the Nginx configuration and restart Nginx**:
    ```bash
    sudo ln -s /etc/nginx/sites-available/backend_project /etc/nginx/sites-enabled
    sudo systemctl restart nginx
    ```

## Architecture Diagram

Below is the architecture diagram for the project:

```plaintext
+-------------------------------------+
|            Django Backend           |
|-------------------------------------|
|                                     |
|  +-----------------------------+    |
|  |       Django REST API       |    |
|  |-----------------------------|    |
|  |  - User Authentication      |    |
|  |  - Post Management          |    |
|  +-----------------------------+    |
|                                     |
|              SQLite                 |
+-------------------------------------+

            +      +
            |      |
            v      v

+-------------------------------------+
|           Frontend Clients          |
|-------------------------------------|
|  - React Application                |
|  - Postman (for testing)            |
+-------------------------------------+

            +      +
            |      |
            v      v

+-------------------------------------+
|               Deployment            |
|-------------------------------------|
|  - AWS EC2                          |
|  - Nginx                            |
|  - Gunicorn                         |
+-------------------------------------+
