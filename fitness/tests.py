from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Exercise, WorkoutPlan, WorkoutLog
from datetime import date


class ExerciseModelTest(TestCase):
    def setUp(self):
        self.exercise = Exercise.objects.create(
            name='Push Up',
            description='Upper body exercise',
            category='strength',
            duration_minutes=30,
            calories_burned=100
        )

    def test_exercise_created(self):
        self.assertEqual(self.exercise.name, 'Push Up')

    def test_exercise_str(self):
        self.assertEqual(str(self.exercise), 'Push Up')


class WorkoutPlanModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.exercise = Exercise.objects.create(
            name='Squat',
            description='Leg exercise',
            category='strength',
            duration_minutes=20,
            calories_burned=80
        )
        self.plan = WorkoutPlan.objects.create(
            user=self.user,
            title='My Plan',
            description='Test plan'
        )
        self.plan.exercises.add(self.exercise)

    def test_plan_created(self):
        self.assertEqual(self.plan.title, 'My Plan')

    def test_plan_user_relationship(self):
        self.assertEqual(self.plan.user, self.user)

    def test_plan_exercise_relationship(self):
        self.assertIn(self.exercise, self.plan.exercises.all())


class WorkoutLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        self.exercise = Exercise.objects.create(
            name='Running',
            description='Cardio exercise',
            category='cardio',
            duration_minutes=45,
            calories_burned=300
        )
        self.plan = WorkoutPlan.objects.create(
            user=self.user,
            title='Cardio Plan',
            description='Cardio plan'
        )
        self.log = WorkoutLog.objects.create(
            user=self.user,
            workout_plan=self.plan,
            date_completed=date.today(),
            duration_minutes=45,
            notes='Good workout'
        )

    def test_log_created(self):
        self.assertEqual(self.log.duration_minutes, 45)

    def test_log_user_relationship(self):
        self.assertEqual(self.log.user, self.user)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser3',
            password='testpass123'
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_functionality(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser3',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_exercise_list_page(self):
        response = self.client.get(reverse('exercise_list'))
        self.assertEqual(response.status_code, 200)

    def test_plan_list_requires_login(self):
        response = self.client.get(reverse('plan_list'))
        self.assertEqual(response.status_code, 302)
