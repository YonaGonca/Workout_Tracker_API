# Workout Tracker API

## Description
REST API developed with Django and Django Rest Framework that allows managing workout routines, exercises, and schedules.
It includes JWT authentication and OpenAPI documentation with Swagger.

## Technologies Used
- Django
- Django Rest Framework (DRF)
- PostgreSQL
- drf-spectacular (for OpenAPI documentation in Swagger)
- Simple JWT (for authentication)
- ReportLab (for generating PDF reports)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-user/workout_project.git
    cd workout_project
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure the PostgreSQL database in `settings.py`:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_user',
            'PASSWORD': 'your_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

5. Apply migrations and load initial data:
    ```bash
    python manage.py migrate
    python manage.py loaddata fixtures/exercises.json  # Optional, loads predefined exercises
    ```

6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

7. Start the server:
    ```bash
    python manage.py runserver
    ```

## Main Endpoints

| Method  | Endpoint                        | Description                          |
|---------|--------------------------------|--------------------------------------|
| GET     | /api/exercises/                | List all exercises                  |
| POST    | /api/exercises/                | Create a new exercise               |
| GET     | /api/exercises/{id}/           | Get exercise details                |
| PUT     | /api/exercises/{id}/           | Update an exercise                  |
| DELETE  | /api/exercises/{id}/           | Delete an exercise                  |
| GET     | /api/workout/                  | List user workouts                  |
| POST    | /api/workout/                  | Create a workout                    |
| GET     | /api/workout/{id}/             | Get workout details                 |
| PUT     | /api/workout/{id}/             | Update a workout                    |
| DELETE  | /api/workout/{id}/             | Delete a workout                    |
| GET     | /api/workout-schedules/        | List workout schedules              |
| POST    | /api/workout-schedules/        | Create a workout schedule           |
| GET     | /api/workout-reports/export_csv/ | Export report in CSV               |
| GET     | /api/workout-reports/export_pdf/ | Export report in PDF               |
| GET     | /api/users/                    | List all users                      |
| POST    | /api/users/register/           | Register a new user                 |
| POST    | /api/users/login/           | Log in a user                 |
| POST    | /api/users/logout/           | Log out a user                 |

                     

## Authentication

This project uses JWT-based authentication. To obtain an access token:

```bash
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_user", "password": "your_password"}'
```

Expected response:
```json
{
    "refresh": "refresh_token",
    "access": "access_token"
}
```

To access protected endpoints, use the access token in the `Authorization` header:
```bash
curl -H "Authorization: Bearer access_token" http://localhost:8000/api/exercises/
```

## API Documentation
API documentation is available in Swagger:
- Swagger UI: [http://localhost:8000/api/schema/swagger/](http://localhost:8000/api/schema/swagger/)

## Tests
Run automated tests with:
```bash
python manage.py test
```

## Contribution
If you want to contribute, feel free to fork the repository and submit a pull request.

## Acknowledgments
- Python for providing the tools to develop this API.
- [roadmap.sh](https://roadmap.sh/projects/fitness-workout-tracker) for inspiring project ideas.
- Django and the open-source community for their documentation and support.
- PostgreSQL for its reliability and performance in managing databases.

## License
This project is licensed under the MIT License.

