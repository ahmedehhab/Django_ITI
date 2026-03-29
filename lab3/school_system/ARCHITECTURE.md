# School App Architecture Summary

## Overview
The school app has been restructured to follow a professional **API App Architecture** pattern, matching the structure of the existing `api` app in the project.

## Architecture Pattern

The app now uses a **layered architecture** with three different view patterns:

### 1. Function-based Views (Simple CRUD)
Used for straightforward operations like creating and retrieving all items.

**Pattern:**
```python
@api_view(["METHOD"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def operation_name(request):
    # Implementation
```

**Benefits:**
- Simple and readable
- Perfect for single operation endpoints
- Minimal boilerplate

**Examples in School App:**
- `register()` - User registration with token
- `login()` - User authentication with token
- `logout()` - User logout (token deletion)
- `create_student()` - Create new student
- `get_all_students()` - Get all students
- `create_subject()` - Create new subject
- `get_all_subjects()` - Get all subjects
- `create_grade()` - Create new grade
- `get_all_grades()` - Get all grades

**Endpoints:**
- POST `/api/register/`
- POST `/api/login/`
- POST `/api/logout/`
- POST `/api/students/create/`
- GET `/api/students/all/`
- POST `/api/subjects/create/`
- GET `/api/subjects/all/`
- POST `/api/grades/create/`
- GET `/api/grades/all/`

---

### 2. APIView Classes (Detail Operations)
Used for operations on specific resources (GET by ID, PUT, DELETE).

**Pattern:**
```python
class ResourceDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, resource_id):
        # Retrieve resource
    
    def put(self, request, resource_id):
        # Update resource
    
    def delete(self, request, resource_id):
        # Delete resource
```

**Benefits:**
- Clear separation of HTTP methods
- Better error handling with try/except
- Consistent status codes and messaging
- Fine-grained control over each operation

**Classes in School App:**
- `StudentDetailView` - Student GET/PUT/DELETE
- `SubjectDetailView` - Subject GET/PUT/DELETE
- `GradeDetailView` - Grade GET/PUT/DELETE

**Endpoints:**
- GET `/api/students/<student_id>/`
- PUT `/api/students/<student_id>/`
- DELETE `/api/students/<student_id>/`
- GET `/api/subjects/<subject_id>/`
- PUT `/api/subjects/<subject_id>/`
- DELETE `/api/subjects/<subject_id>/`
- GET `/api/grades/<grade_id>/`
- PUT `/api/grades/<grade_id>/`
- DELETE `/api/grades/<grade_id>/`

---

### 3. ModelViewSets (Advanced Filtering)
Used for complex queries with filtering, searching, ordering, and pagination.

**Pattern:**
```python
class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['field1', 'field2']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'date']
    ordering = ['name']
```

**Benefits:**
- Automatically handles list and detail views
- Built-in filtering, searching, ordering
- Pagination support
- Minimal code required
- Router-based URL generation

**ViewSets in School App:**
- `StudentViewSet` - Advanced student filtering
- `SubjectViewSet` - Advanced subject filtering
- `GradeViewSet` - Advanced grade filtering

**Endpoints (v2):**
- GET `/api/students-v2/?age=20&search=john&ordering=name`
- GET `/api/subjects-v2/?name=Math&search=calculus`
- GET `/api/grades-v2/?student=1&score=85&ordering=-score`

---

## Authentication Strategy

**Token-based Authentication**

All endpoints (except `register`) require a valid authentication token.

**Flow:**
1. User calls `/api/register/` → Receives token
2. OR User calls `/api/login/` → Receives token
3. User includes token in Authorization header: `Authorization: Token <token>`
4. User calls `/api/logout/` → Token is deleted

**Advantages:**
- Stateless (suitable for mobile apps, SPAs, third-party clients)
- No session management needed
- Security tokens can be revoked
- Works across devices

---

## File Structure

```
school/
├── models.py          # Data models (Student, Subject, Grade)
├── serializers.py     # DRF serializers (StudentSerializer, SubjectSerializer, GradeSerializer)
├── views.py           # All view patterns:
│                      #   - Function-based (register, login, create_*, get_all_*)
│                      #   - APIView classes (StudentDetailView, SubjectDetailView, GradeDetailView)
│                      #   - ModelViewSets (StudentViewSet, SubjectViewSet, GradeViewSet)
├── urls.py            # URL routing with router registration
├── signals.py         # Django signals (removed)
├── apps.py            # App config with signal registration
├── admin.py
├── tests.py
├── forms.py           # (Legacy, not used in REST API)
└── migrations/        # Database migrations
```

---

---

## Request/Response Patterns

### Successful Create (201)
```json
{
  "msg": "Student created successfully.",
  "data": { "id": 1, "name": "John", "age": 20, "email": "john@example.com", "image": null }
}
```

### Successful Get (200)
```json
{
  "msg": "Student retrieved successfully.",
  "data": { "id": 1, "name": "John", "age": 20, "email": "john@example.com", "image": null }
}
```

### Successful List (200)
```json
{
  "msg": "Students retrieved successfully.",
  "data": [
    { "id": 1, "name": "John", "age": 20, "email": "john@example.com", "image": null },
    { "id": 2, "name": "Jane", "age": 19, "email": "jane@example.com", "image": null }
  ]
}
```

### Successful Update (200)
```json
{
  "msg": "Student updated successfully.",
  "data": { "id": 1, "name": "John Updated", "age": 21, "email": "john@example.com", "image": null }
}
```

### Successful Delete (200)
```json
{
  "msg": "Student deleted successfully."
}
```

### Error Response (400/401/404)
```json
{
  "error": "Error description",
  "details": { "field": ["error message"] }
}
```

---

## Comparison: Old vs New Architecture

| Aspect | Old | New |
|--------|-----|-----|
| **Views** | Template-based + ViewSets only | Function-based + APIView + ViewSets |
| **Authentication** | Session-based | Token-based |
| **Auth Endpoints** | None | register/login/logout |
| **Create Operation** | POST to `/students/` via ViewSet | POST to `/students/create/` via function |
| **Get Details** | GET `/students/1/` via ViewSet | GET `/students/1/` via APIView |
| **List All** | GET `/students/` via ViewSet | GET `/students/all/` via function |
| **Advanced Filter** | `/students/?search=...` | `/students-v2/?search=...` |
| **Templates** | HTML templates | None (API only) |
| **Response Format** | Paginated list | Consistent `{msg, data}` format |

---

## Developer Guide

### Adding a New Endpoint

**Example: Add a new endpoint to get students by age range**

1. **Add to function-based views** in `views.py`:
```python
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_students_by_age_range(request):
    min_age = request.query_params.get('min')
    max_age = request.query_params.get('max')
    
    if not min_age or not max_age:
        return Response({"error": "min and max age required"}, status=400)
    
    students = Student.objects.filter(age__gte=min_age, age__lte=max_age)
    serializer = StudentSerializer(students, many=True)
    return Response({"msg": "Students retrieved.", "data": serializer.data}, status=200)
```

2. **Add to URLs** in `urls.py`:
```python
path('students/by-age-range/', views.get_students_by_age_range, name='get_students_by_age_range'),
```

3. **Test**:
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/students/by-age-range/?min=18&max=25"
```

---

## Best Practices Followed

1. **Consistent naming conventions**
   - Function views: `create_*`, `get_*`, `get_all_*`
   - Classes: `*DetailView`, `*ViewSet`

2. **Proper HTTP status codes**
   - 200: OK
   - 201: Created
   - 400: Bad Request
   - 401: Unauthorized
   - 404: Not Found

3. **Standardized response format**
   - All responses have `msg` (success) or `error` (failure)
   - Data payload in `data` field

4. **Authentication everywhere**
   - All API endpoints require token authentication
   - Except public endpoints (register available without auth)

5. **DRY principle**
   - Serializers handle validation and data transformation

6. **Modular structure**
   - Three view patterns for different use cases
   - Easy to extend and maintain

---

## Performance Considerations

1. **Select Related**: Used in Grade queries to reduce database hits
   ```python
   Grade.objects.select_related('student', 'subject')
   ```

2. **Pagination**: Default 10 items per page for large lists

3. **Filtering**: Use indexed fields (`age`, `email`, `code`)

4. **Search**: Implemented on text fields only

---

## Testing the API

```bash
# Register
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123","email":"test@example.com"}'

# Login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# Create Student
curl -X POST http://localhost:8000/api/students/create/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","age":20,"email":"alice@example.com"}'

# Get All Students
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/students/all/

# Get Student Details
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/students/1/

# Update Student
curl -X PUT http://localhost:8000/api/students/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Updated","age":21}'

# Delete Student
curl -X DELETE http://localhost:8000/api/students/1/ \
  -H "Authorization: Token YOUR_TOKEN"

# Advanced Filter
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/students-v2/?search=alice&ordering=name"

# Logout
curl -X POST http://localhost:8000/api/logout/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

---

## Next Steps

The school app is now fully converted to a professional API app architecture. You can:

1. Deploy to production (update ALLOWED_HOSTS, DEBUG=False, SECRET_KEY)
2. Add more complex business logic in view layers
3. Extend with additional endpoints as needed
4. Integrate with frontend framework (React, Vue, Angular)
5. Add rate limiting, pagination customization
6. Implement caching strategies
