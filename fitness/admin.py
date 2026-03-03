from django.contrib import admin
from .models import Exercise, WorkoutPlan, WorkoutLog


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'duration_minutes', 'calories_burned']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    list_filter = ['user']
    search_fields = ['title']


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout_plan', 'date_completed', 'duration_minutes']
    list_filter = ['user', 'date_completed']
