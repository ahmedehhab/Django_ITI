from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Student, Subject, Grade
from .serializers import StudentSerializer, SubjectSerializer, GradeSerializer, UserSerializer


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    
    if not username or not password or not email:
        return Response(
            {"error": "Username, password and email are required."}, 
            status=400
        )
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists."}, 
            status=400
        )
    
    user = User.objects.create_user(username=username, password=password, email=email)
    token = Token.objects.create(user=user)
    return Response(
        {"msg": "User registered successfully.", "token": token.key, "user": UserSerializer(user).data}, 
        status=201
    )


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    if not username or not password:
        return Response(
            {"error": "Username and password are required."}, 
            status=400
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response(
            {"msg": "Login successful.", "token": token.key, "user": UserSerializer(user).data}, 
            status=200
        )
    else:
        return Response(
            {"error": "Invalid credentials."}, 
            status=401
        )



@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"msg": "Student created successfully.", "data": serializer.data}, 
            status=201
        )
    return Response(
        {"error": "Invalid data.", "details": serializer.errors}, 
        status=400
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(
        {"msg": "Students retrieved successfully.", "data": serializer.data}, 
        status=200
    )


class StudentDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            serializer = StudentSerializer(student)
            return Response(
                {"msg": "Student retrieved successfully.", "data": serializer.data}, 
                status=200
            )
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found."}, 
                status=404
            )

    def put(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "Student updated successfully.", "data": serializer.data}, 
                    status=200
                )
            return Response(
                {"error": "Invalid data.", "details": serializer.errors}, 
                status=400
            )
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found."}, 
                status=404
            )

    def delete(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            student.delete()
            return Response(
                {"msg": "student deleted successfully"}, 
                status=200
            )
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found."}, 
                status=404
            )


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['age', 'email']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'age']
    ordering = ['name']



@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_subject(request):
    serializer = SubjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"msg": "subject created successfully", "data": serializer.data}, 
            status=201
        )
    return Response(
        {"error": "invalid data", "details": serializer.errors}, 
        status=400
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_subjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(
        {"msg": "subjects retrieved successfully", "data": serializer.data}, 
        status=200
    )


class SubjectDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        """Get subject details"""
        try:
            subject = Subject.objects.get(id=subject_id)
            serializer = SubjectSerializer(subject)
            return Response(
                {"msg": "subject retrieved successfully", "data": serializer.data}, 
                status=200
            )
        except Subject.DoesNotExist:
            return Response(
                {"error": "subject not found"}, 
                status=404
            )

    def put(self, request, subject_id):
        try:
            subject = Subject.objects.get(id=subject_id)
            serializer = SubjectSerializer(subject, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "subject updated successfully", "data": serializer.data}, 
                    status=200
                )
            return Response(
                {"error": "invalid data", "details": serializer.errors}, 
                status=400
            )
        except Subject.DoesNotExist:
            return Response(
                {"error": "subject not found"}, 
                status=404
            )

    def delete(self, request, subject_id):
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.delete()
            return Response(
                {"msg": "Subject deleted successfully"}, 
                status=200
            )
        except Subject.DoesNotExist:
            return Response(
                {"error": "Subject not found"}, 
                status=404
            )


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'code']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    ordering = ['name']



@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_grade(request):
    """Create a new grade"""
    serializer = GradeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"msg": "Grade created successfully.", "data": serializer.data}, 
            status=201
        )
    return Response(
        {"error": "Invalid data.", "details": serializer.errors}, 
        status=400
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_grades(request):
    """Get all grades"""
    grades = Grade.objects.select_related('student', 'subject').all()
    serializer = GradeSerializer(grades, many=True)
    return Response(
        {"msg": "Grades retrieved successfully.", "data": serializer.data}, 
        status=200
    )


class GradeDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, grade_id):
        """Get grade details"""
        try:
            grade = Grade.objects.select_related('student', 'subject').get(id=grade_id)
            serializer = GradeSerializer(grade)
            return Response(
                {"msg": "Grade retrieved successfully.", "data": serializer.data}, 
                status=200
            )
        except Grade.DoesNotExist:
            return Response(
                {"error": "Grade not found."}, 
                status=404
            )

    def put(self, request, grade_id):
        try:
            grade = Grade.objects.get(id=grade_id)
            serializer = GradeSerializer(grade, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "Grade updated successfully.", "data": serializer.data}, 
                    status=200
                )
            return Response(
                {"error": "Invalid data.", "details": serializer.errors}, 
                status=400
            )
        except Grade.DoesNotExist:
            return Response(
                {"error": "Grade not found."}, 
                status=404
            )

    def delete(self, request, grade_id):
        try:
            grade = Grade.objects.get(id=grade_id)
            grade.delete()
            return Response(
                {"msg": "Grade deleted successfully."}, 
                status=200
            )
        except Grade.DoesNotExist:
            return Response(
                {"error": "Grade not found."}, 
                status=404
            )


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related('student', 'subject').all()
    serializer_class = GradeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student', 'subject', 'score']
    search_fields = ['student__name', 'subject__name']
    ordering_fields = ['score', 'student__name', 'subject__name']
    ordering = ['-score']