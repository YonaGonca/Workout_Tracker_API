from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import Exercise, Workout, WorkoutSchedule
from .serializers import ExerciseSerializer, UserSerializer, RegisterSerializer, WorkoutSerializer, WorkoutScheduleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.filters import OrderingFilter
from django.http import JsonResponse, HttpResponse
import csv
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas

# Exercise Viewset
@extend_schema_view(
    list=extend_schema(description="Retrieve the list of exercises"),
    retrieve=extend_schema(description="Retrieve an exercise by ID"),
    create=extend_schema(description="Create a new exercise"),
    update=extend_schema(description="Update an exercise"),
    destroy=extend_schema(description="Delete an exercise")
    )
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

# User Viewset
@extend_schema_view(
    list=extend_schema(description="Retrieve the list of users"),
    retrieve=extend_schema(description="Retrieve a user by ID"),
    register=extend_schema(description="Register a new user"),
    login=extend_schema(description="User login"),
    logout=extend_schema(description="User logout")
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response({"error": "Invalid credentials."}, status=400)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def logout(self, request):
        refresh_token = request.data.get("refresh")  
        if not refresh_token:
            return Response({"error": "No refresh token provided."}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response({"message": "Logout successful."}, status=205)
        except Exception:
            return Response({"error": "Invalid token."}, status=400)

# Workout Viewset
@extend_schema_view(
    list=extend_schema(description="Retrieve user workouts"),
    retrieve=extend_schema(description="Retrieve a workout by ID"),
    create=extend_schema(description="Create a new workout"),
    update=extend_schema(description="Update a workout"),
    destroy=extend_schema(description="Delete a workout")
)
class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Workout Schedule Viewset
@extend_schema_view(
    list=extend_schema(description="Retrieve the schedule of workouts"),
    retrieve=extend_schema(description="Retrieve a workout schedule by ID"),
    create=extend_schema(description="Create a new workout schedule"),
    update=extend_schema(description="Update a workout schedule"),
    destroy=extend_schema(description="Delete a workout schedule")
)
class WorkoutScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutScheduleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['scheduled_at']
    ordering = ['scheduled_at']

    def get_queryset(self):
        return WorkoutSchedule.objects.filter(workout__user=self.request.user)

# Report Viewset
@extend_schema_view(
    export_csv=extend_schema(description="Export workout reports in CSV format"),
    export_pdf=extend_schema(description="Export workout reports in PDF format")
)
class WorkoutReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_past_schedules(self, request):
        return WorkoutSchedule.objects.filter(workout__user=request.user, scheduled_at__lt=timezone.now())

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        past_schedules = self.get_past_schedules(request)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="workout_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Workout Name', 'Scheduled At'])
        for schedule in past_schedules:
            writer.writerow([schedule.workout.name, schedule.scheduled_at.strftime("%Y-%m-%d %H:%M")])
        return response

    @action(detail=False, methods=['get'])
    def export_pdf(self, request):
        past_schedules = self.get_past_schedules(request)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="workout_report.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica", 12)
        p.drawString(100, 800, f"Workout Report for {request.user.username}")
        y_position = 780
        for schedule in past_schedules:
            y_position -= 20
            p.drawString(100, y_position, f"Workout: {schedule.workout.name} - {schedule.scheduled_at.strftime('%Y-%m-%d %H:%M')}")
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

