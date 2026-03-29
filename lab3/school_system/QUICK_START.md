# Quick Start Guide - School API

## Project Structure

```
school_system/
├── api/                    # Existing reference API app
├── school/                 # Your main app (converted to API app architecture)
│   ├── models.py          # Student, Subject, Grade models
│   ├── serializers.py     # DRF serializers + UserSerializer
│   ├── views.py           # Function-based, APIView, and ViewSets
│   ├── urls.py            # API routing + router
│   ├── signals.py         # (removed)
│   ├── apps.py            # Signal registration
│   └── migrations/        # Database migrations
├── school_system/         # Project settings
│   ├── settings.py        # Updated with authtoken
│   ├── urls.py            # Include school URLs
│   └── wsgi.py
├── manage.py
├── db.sqlite3
├── API_DOCUMENTATION.md   # Full API reference
└── ARCHITECTURE.md        # Architecture details
```

## Start the Server

```bash
cd /home/ahmed/Desktop/Django_ITI/school_system
source venv/bin/activate
python manage.py runserver
```

Default URL: `http://localhost:8000/api/`

## View Types in School App

### 1️⃣ Function-based Views
Simple operations (auth, create, list all)
```
POST   /api/register/         - Register user
POST   /api/login/            - Login & get token
POST   /api/logout/           - Logout user
POST   /api/students/create/  - Create student
GET    /api/students/all/     - Get all students
POST   /api/subjects/create/  - Create subject
GET    /api/subjects/all/     - Get all subjects
POST   /api/grades/create/    - Create grade
GET    /api/grades/all/       - Get all grades
```

### 2️⃣ APIView Classes
Detail operations (get, update, delete by ID)
```
GET    /api/students/{id}/    - Get details
PUT    /api/students/{id}/    - Update
DELETE /api/students/{id}/    - Delete
GET    /api/subjects/{id}/    - Get details
PUT    /api/subjects/{id}/    - Update
DELETE /api/subjects/{id}/    - Delete
GET    /api/grades/{id}/      - Get details
PUT    /api/grades/{id}/      - Update
DELETE /api/grades/{id}/      - Delete
```

### 3️⃣ ModelViewSets
Advanced filtering (with v2 suffix)
```
GET    /api/students-v2/      - Filter: age, email | Search: name, email
GET    /api/subjects-v2/      - Filter: name, code | Search: name, code, description
GET    /api/grades-v2/        - Filter: student, subject, score | Search: student, subject
```

## Authentication

All endpoints require Token authentication (except register).

**Get Token:**
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "password123",
    "email": "student@example.com"
  }'
```

Response will include your token.

**Use Token:**
```bash
curl -H "Authorization: Token YOUR_TOKEN_HERE" \
  http://localhost:8000/api/students/all/
```

## Quick Test Sequence

```bash
# 1. Register
TOKEN=$(curl -s -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123","email":"test@example.com"}' \
  | jq -r '.token')

# 2. Create student
curl -X POST http://localhost:8000/api/students/create/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","age":20,"email":"john@example.com"}'

# 3. Get all students
curl -H "Authorization: Token $TOKEN" \
  http://localhost:8000/api/students/all/

# 4. Create subject
curl -X POST http://localhost:8000/api/subjects/create/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Math","code":"MATH101","description":"Mathematics"}'

# 5. Create grade
curl -X POST http://localhost:8000/api/grades/create/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"student":1,"subject":1,"score":85}'

# 6. Get grades with advanced filter
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/grades-v2/?ordering=-score"

# 7. Get student detail
curl -H "Authorization: Token $TOKEN" \
  http://localhost:8000/api/students/1/

# 8. Update student
curl -X PUT http://localhost:8000/api/students/1/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated","age":21}'

# 9. Delete student
curl -X DELETE http://localhost:8000/api/students/1/ \
  -H "Authorization: Token $TOKEN"

# 10. Logout
curl -X POST http://localhost:8000/api/logout/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

## Key Features

✅ **Token Authentication** - Secure, stateless auth  
✅ **Three View Patterns** - Function, APIView, ViewSet  
✅ **Token Authentication** - Secure, stateless auth  
✅ **Filtering** - Advanced search and filter on v2 endpoints  
✅ **Pagination** - 10 items per page  
✅ **Error Handling** - Consistent JSON responses  

## Response Format

### Success (Create)
```json
{
  "msg": "Student created successfully.",
  "data": { "id": 1, "name": "John", "age": 20, "email": "john@example.com", "image": null }
}
```

### Success (List)
```json
{
  "msg": "Students retrieved successfully.",
  "data": [
    { "id": 1, "name": "John", "age": 20, "email": "john@example.com", "image": null }
  ]
}
```

### Error
```json
{
  "error": "Error description",
  "details": { "field": ["validation error"] }
}
```

## Important URLs

- **API Base**: `http://localhost:8000/api/`
- **Docs**: See `API_DOCUMENTATION.md`
- **Architecture**: See `ARCHITECTURE.md`

## Admin Panel

```bash
# Create superuser (if needed)
python manage.py createsuperuser

# Then visit: http://localhost:8000/admin/
```

## Troubleshooting

**Issue**: Port 8000 already in use
```bash
# Use a different port
python manage.py runserver 8001
```

**Issue**: Database errors
```bash
# Reset migrations (warning: deletes data)
python manage.py migrate school zero
python manage.py migrate
```

**Issue**: Missing dependencies
```bash
# Reinstall requirements
pip install -r requirements.txt
```

## File Modifications Summary

- `school/views.py` - Complete rewrite with 3 view patterns
- `school/urls.py` - Updated routing with router
- `school/serializers.py` - Updated for token auth
- `school/apps.py` - Added signal registration
- `school_system/settings.py` - Added authtoken app & DRF config
- `school/signals.py` - Removed (signals deleted)

## Next Steps

1. Deploy to production (update settings)
2. Add rate limiting
3. Integrate with frontend (React, Vue, etc.)
4. Add custom business logic
5. Add more endpoints

---

**Enjoy your fully-structured API app! 🚀**
