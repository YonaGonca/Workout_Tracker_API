from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    muscle_group = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    repetitions = models.IntegerField()
    weight = models.FloatField()
    
    def __str__(self):
        return f'{self.exercise.name} - {self.sets}x{self.reps} at {self.weight} kg'    
    
class WorkoutSchedule(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='schedules')
    scheduled_at = models.DateTimeField()
    
    def __str__(self):
        return f'{self.workout.name} scheduled at {self.scheduled_at}'