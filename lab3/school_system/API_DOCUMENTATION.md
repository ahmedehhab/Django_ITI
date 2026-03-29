# School System API Documentation

This is a RESTful API for managing students, subjects, and grades in a school system using Token-based authentication.

## Installation & Setup

### Installed Dependencies
- Django REST Framework
- django-filter
- djangorestframework (authtoken)

### Project Structure (API App Architecture)

The school app follows a professional API app architecture pattern with:
- **Function-based views** with decorators for specific CRUD operations
- **APIView classes** for detailed operations (GET, PUT, DELETE by ID)
- **ModelViewSets** for advanced filtering and list operations
- **Token-based authentication** for secure API access
- **Signal handlers** for model event logging

## Authentication

The API uses Token-based authentication. Each user gets an authentication token upon registration or login.

### Get Authentication Token

#### Register a New User
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "secure_password",
    "email": "student@example.com"
  }'
```

Response:
```json
{
  "msg": "User registered successfully.",
  "token": "9944b09199c62bcf9418ad846dd0e4bbea6f939f",
  "user": {
    "id": 1,
    "username": "student1",
    "email": "student@example.com"
  }
}
```

#### Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "secure_password"
  }'
```

#### Logout
```bash
curl -X POST http://localhost:8000/api/logout/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "secure_password"
  }'
```

### Using Token in Requests

Include your token in the Authorization header for all authenticated requests:

```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6f939f" \
  http://localhost:8000/api/students/all/
```

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

---

## STUDENTS ENDPOINTS

### Create Student (Function-based View)
- **POST** `/api/students/create/`
- **Authentication**: Token required
- **Content-Type**: application/json

Request:
```json
{
  "name": "John Doe",
  "age": 20,
  "email": "john@example.com",
  "image": null
}
```

Response (201 Created):
```json
{
  "msg": "Student created successfully.",
  "data": {
    "id": 1,
    "name": "John Doe",
    "age": 20,
    "email": "john@example.com",
    "image": null
  }
}
```

### Get All Students (Function-based View)
- **GET** `/api/students/all/`
- **Authentication**: Token required

Response (200 OK):
```json
{
  "msg": "Students retrieved successfully.",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "age": 20,
      "email": "john@example.com",
      "image": null
    }
  ]
}
```

### Get Student Details (APIView Class)
- **GET** `/api/students/{student_id}/`
- **Authentication**: Token required

### Update Student (APIView Class)
- **PUT** `/api/students/{student_id}/`
- **Authentication**: Token required
- **Content-Type**: application/json

### Delete Student (APIView Class)
- **DELETE** `/api/students/{student_id}/`
- **Authentication**: Token required

### Advanced Student Filtering (ModelViewSet)
- **GET** `/api/students-v2/`
- **Query Parameters**:
  - `age=20` - Filter by age
  - `email=john@example.com` - Filter by email
  - `search=john` - Search by name or email
  - `ordering=name` or `ordering=age` - Order results
  - `page=1` - Pagination

Example:
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/students-v2/?search=john&ordering=name"
```

---

## SUBJECTS ENDPOINTS

### Create Subject (Function-based View)
- **POST** `/api/subjects/create/`
- **Authentication**: Token required

Request:
```json
{
  "name": "Mathematics",
  "code": "MATH101",
  "description": "Introduction to Mathematics"
}
```

### Get All Subjects (Function-based View)
- **GET** `/api/subjects/all/`
- **Authentication**: Token required

### Get Subject Details (APIView Class)
- **GET** `/api/subjects/{subject_id}/`
- **Authentication**: Token required

### Update Subject (APIView Class)
- **PUT** `/api/subjects/{subject_id}/`
- **Authentication**: Token required

### Delete Subject (APIView Class)
- **DELETE** `/api/subjects/{subject_id}/`
- **Authentication**: Token required

### Advanced Subject Filtering (ModelViewSet)
- **GET** `/api/subjects-v2/`
- **Query Parameters**:
  - `name=Math` - Filter by name
  - `code=MATH101` - Filter by code
  - `search=mathematics` - Search by name, code, or description
  - `ordering=name` or `ordering=code` - Order results
  - `page=1` - Pagination

---

## GRADES ENDPOINTS

### Create Grade (Function-based View)
- **POST** `/api/grades/create/`
- **Authentication**: Token required

Request:
```json
{
  "student": 1,
  "subject": 1,
  "score": 85
}
```

Constraints:
- Score must be between 0 and 100

### Get All Grades (Function-based View)
- **GET** `/api/grades/all/`
- **Authentication**: Token required

Response includes nested `student_name` and `subject_name` fields.

### Get Grade Details (APIView Class)
- **GET** `/api/grades/{grade_id}/`
- **Authentication**: Token required

### Update Grade (APIView Class)
- **PUT** `/api/grades/{grade_id}/`
- **Authentication**: Token required

### Delete Grade (APIView Class)
- **DELETE** `/api/grades/{grade_id}/`
- **Authentication**: Token required

### Advanced Grade Filtering (ModelViewSet)
- **GET** `/api/grades-v2/`
- **Query Parameters**:
  - `student=1` - Filter by student ID
  - `subject=1` - Filter by subject ID
  - `score=85` - Filter by score
  - `search=john` - Search by student or subject name
  - `ordering=score` or `ordering=-score` - Order by score (descending with -)
  - `ordering=student__name` - Order by student name
  - `page=1` - Pagination

Example:
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/grades-v2/?student=1&ordering=-score"
```

---

## Response Format Standards

### Success Response (List/All)
```json
{
  "msg": "Items retrieved successfully.",
  "data": [...]
}
```

### Success Response (Create)
```json
{
  "msg": "Item created successfully.",
  "data": {...}
}
```

### Success Response (Update)
```json
{
  "msg": "Item updated successfully.",
  "data": {...}
}
```

### Success Response (Delete)
```json
{
  "msg": "Item deleted successfully."
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": {...}  // Only for validation errors
}
```

---

## Architecture Patterns Used

### 1. Function-based Views with Decorators
Used for simple create and get_all operations:
```python
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_student(request):
    # Implementation
```

**Advantages**: Simple, readable, perfect for straightforward operations.

### 2. APIView Classes
Used for detail operations (GET by ID, PUT, DELETE):
```python
class StudentDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id):
        # Get implementation
    
    def put(self, request, student_id):
        # Update implementation
    
    def delete(self, request, student_id):
        # Delete implementation
```

**Advantages**: Fine-grained control, good for handling multiple HTTP methods.

### 3. ModelViewSets
Used for advanced filtering and listing:
```python
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['age', 'email']
    search_fields = ['name', 'email']
```

**Advantages**: Powerful filtering, searching, ordering, pagination with minimal code.

### 4. Token-based Authentication
Secure, stateless authentication suitable for mobile and third-party clients.

### 5. Django Signals
Signals have been removed from this project.

---

## Example Workflow

1. **Register User**
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123","email":"admin@example.com"}'
```
Get token from response.

2. **Create Student**
```bash
curl -X POST http://localhost:8000/api/students/create/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","age":18,"email":"alice@example.com"}'
```

3. **Search Students**
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/students-v2/?search=alice"
```

4. **Get Student Details**
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/students/1/
```

5. **Update Student**
```bash
curl -X PUT http://localhost:8000/api/students/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Johnson","age":19}'
```

6. **Delete Student**
```bash
curl -X DELETE http://localhost:8000/api/students/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```

---

## Running the Server

```bash
cd /home/ahmed/Desktop/Django_ITI/school_system
source venv/bin/activate
python manage.py runserver
```

API will be available at: `http://localhost:8000/api/`

---

## Pagination

List endpoints return paginated results (10 items per page by default).

Response includes:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/students-v2/?page=2",
  "previous": null,
  "results": [...]
}
```

Navigate with `?page=2`, `?page=3`, etc.

---

## HTTP Status Codes

- `200 OK` - Successful GET/PUT/DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Invalid data, missing required fields
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Notes

- All authenticated endpoints require a valid Token
- Images for students are stored in `media/students/`
- Grade scores must be integers between 0-100
- Pagination defaults to 10 items per page
- Use `-v2` endpoints for advanced filtering needs

