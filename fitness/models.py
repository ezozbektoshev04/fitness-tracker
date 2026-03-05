from django.db import models
from django.contrib.auth.models import User


class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
        ('flexibility', 'Flexibility'),
        ('balance', 'Balance'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    # MANY-TO-ONE: many plans can belong to one user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')
    title = models.CharField(max_length=200)
    description = models.TextField()
    # MANY-TO-MANY: a plan can have many exercises, exercise can be in many plans
    exercises = models.ManyToManyField(Exercise, related_name='workout_plans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class WorkoutLog(models.Model):
    # MANY-TO-ONE: many logs can belong to one user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_logs')
    # MANY-TO-ONE: many logs can reference one workout plan
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='logs')
    date_completed = models.DateField()
    notes = models.TextField(blank=True)
    duration_minutes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout_plan.title} - {self.date_completed}"
