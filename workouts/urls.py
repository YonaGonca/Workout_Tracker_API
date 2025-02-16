from rest_framework import routers
from .api import ExerciseViewSet, UserViewSet, WorkoutViewSet, WorkoutScheduleViewSet, WorkoutReportViewSet

router = routers.DefaultRouter()

router.register('api/exercises', ExerciseViewSet, 'exercises')
router.register('api/users', UserViewSet, 'users')
router.register('api/workout', WorkoutViewSet, 'workouts')
router.register('api/workout-schedules', WorkoutScheduleViewSet, 'workout-schedules')
router.register('api/workout-reports', WorkoutReportViewSet, 'workout-report')   

urlpatterns = router.urls