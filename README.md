# Event Registration API
#### A Django Event Registration API is a backend service built using the Django RestFramework .

## Tools :
- Django
- RestFramework
- Docker
- Celery
- Redis
  
## Featues :
- Register , Token Auth, Reset Password
- Create , update and delete Events by organizer
- Register into events , update registration and delete

## Installation :
  ### Requirements
  - Python (3.x.x)
  - Docker
  - Docker-Compose
  ### SetUp
   - Create database
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
  - Create Admin User (username,password) required
    ```
    python manage.py createsuperuser
    ```
  - Open Docker
  - For Unix and Windows run the following command :
    ```
    docker-compose up --build
    ```
