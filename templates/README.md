# Travel Manager API

A Django REST Framework application for managing travel projects and places to visit.

Users can:
- Create travel projects
- Add places from the Art Institute of Chicago API
- Attach notes to places
- Mark places as visited
- Automatically complete projects when all places are visited

---

# Features

- Django REST Framework API
- Nested project/place endpoints
- External API integration with Art Institute of Chicago API
- Validation of external places before saving
- Maximum 10 places per project
- Prevent duplicate places inside a project
- Automatic project completion logic
- Postman collection included

---

# Tech Stack

- Python 3.12+
- Django
- Django REST Framework
- SQLite
- Requests

---

# Setup Instructions

## 1. Clone repository

```bash
git clone https://github.com/y-kondrashova/travel_manager.git
cd travel_manager
```

---

## 2. Create virtual environment

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5. Start development server

```bash
python manage.py runserver
```

Application will be available at:

```text
http://127.0.0.1:8000/
```

---

# API Endpoints

## Projects

| Method | Endpoint                    | Description |
|---|-----------------------------|---|
| GET | `api/travel/projects/`      | List projects |
| POST | `api/travel/projects/`      | Create project with places |
| GET | `api/travel/projects/{id}/` | Retrieve single project |
| PATCH | `api/travel/projects/{id}/` | Update project |
| DELETE | `api/travel/projects/{id}/` | Delete project |

---

## Places

| Method | Endpoint                                   | Description |
|---|--------------------------------------------|---|
| GET | `api/travel/projects/{project_id}/places/` | List places in project |
| POST | `api/travel/projects/{project_id}/places/`           | Add place to project |
| GET | `api/travel/projects/{project_id}/places/{id}/`      | Retrieve single place |
| PATCH | `api/travel/projects/{project_id}/places/{id}/`      | Update notes/visited |
| DELETE | `api/travel/projects/{project_id}/places/{id}/`      | Delete place |

---

# Example Requests

## Create Project

### POST `api/travel/projects/`

```json
{
  "name": "Chicago Art Trip",
  "description": "Museum planning",
  "start_date": "2026-06-01",
  "places": [
    {
      "external_id": 129884
    },
    {
      "external_id": 27992
    }
  ]
}
```

---

## Add Place to Existing Project

### POST `api/travel/projects/1/places/`

```json
{
  "external_id": 111628,
  "notes": "Must visit first"
}
```

---

## Update Place

### PATCH `api/travel/projects/1/places/1/`

```json
{
  "notes": "Visited on first day",
  "visited": true
}
```
---

# Postman Collection

Postman collection is available in:

```text
https://www.postman.com/spycat/workspace/travel
```

Import the collection into Postman to test all endpoints.
