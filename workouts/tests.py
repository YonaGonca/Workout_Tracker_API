from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Exercise, Workout, WorkoutSchedule

class ExerciseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.exercise = Exercise.objects.create(name='Push Up', description='Upper body exercise', muscle_group='Chest')

    def test_list_exercises(self):
        response = self.client.get('/api/exercises/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_exercise(self):
        data = {'name': 'Squat', 'description': 'Leg exercise', 'muscle_group': 'Legs'}
        response = self.client.post('/api/exercises/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserTests(APITestCase):
    def test_register_user(self):
        data = {
            'username': 'newuser', 
            'email': 'newuser@example.com', 
            'password': 'Str0ngP@ssw0rd!',  # Nueva contraseña más segura
            'password2': 'Str0ngP@ssw0rd!'
        }        
        response = self.client.post('/api/users/register/', data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class WorkoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.workout = Workout.objects.create(user=self.user, name='Morning Routine')

    def test_list_workouts(self):
        response = self.client.get('/api/workout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_workout(self):
        data = {'name': 'Evening Routine'}
        response = self.client.post('/api/workout/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class WorkoutScheduleTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.workout = Workout.objects.create(user=self.user, name='Morning Routine')
        self.schedule = WorkoutSchedule.objects.create(workout=self.workout, scheduled_at='2030-01-01T10:00:00Z')

    def test_list_schedules(self):
        response = self.client.get('/api/workout-schedules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_schedule(self):
        data = {'workout': self.workout.id, 'scheduled_at': '2030-02-01T10:00:00Z'}
        response = self.client.post('/api/workout-schedules/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
