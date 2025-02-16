from rest_framework import serializers
from .models import Exercise, WorkoutExercise, Workout, WorkoutSchedule
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user        
    
class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise', 'sets', 'repetitions', 'weight']
            
class WorkoutScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSchedule
        fields = ['id', 'workout', 'scheduled_at']
        
    def validate_scheduled_at(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Scheduled date/time cannot be in the past.")
        return value
    
class WorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, required=False)
    schedules = WorkoutScheduleSerializer(many=True, required=False, read_only=True)
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'user', 'created_at', 'exercises', 'schedules']
        read_only_fields = ['user', 'created_at']
        
    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises', [])
        workout = Workout.objects.create(**validated_data)
        for exercise_data in exercises_data:
            WorkoutExercise.objects.create(workout=workout, **exercise_data)
        return workout
    
    def update(self, instance, validated_data):
        exercises_data = validated_data.pop('exercises', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if exercises_data is not None:
            instance.exercises.all().delete()
            for exercise_data in exercises_data:
                WorkoutExercise.objects.create(workout=instance, **exercise_data)

        return instance