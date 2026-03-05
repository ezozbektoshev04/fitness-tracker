from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exercise, WorkoutPlan, WorkoutLog
from .forms import WorkoutPlanForm, WorkoutLogForm


# HOME PAGE
def home(request):
    return render(request, 'home.html')


# REGISTER
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# LOGIN
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')


# DASHBOARD
@login_required
def dashboard(request):
    plans = WorkoutPlan.objects.filter(user=request.user)
    logs = WorkoutLog.objects.filter(user=request.user).order_by('-date_completed')[:5]
    total_workouts = logs.count()
    return render(request, 'dashboard.html', {
        'plans': plans,
        'logs': logs,
        'total_workouts': total_workouts,
    })


# EXERCISE LIST
def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'exercise_list.html', {'exercises': exercises})


# WORKOUT PLAN LIST
@login_required
def plan_list(request):
    plans = WorkoutPlan.objects.filter(user=request.user)
    return render(request, 'plan_list.html', {'plans': plans})


# WORKOUT PLAN DETAIL
@login_required
def plan_detail(request, pk):
    plan = get_object_or_404(WorkoutPlan, pk=pk, user=request.user)
    return render(request, 'plan_detail.html', {'plan': plan})


# CREATE WORKOUT PLAN
@login_required
def plan_create(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            form.save_m2m()
            messages.success(request, 'Workout plan created!')
            return redirect('plan_list')
    else:
        form = WorkoutPlanForm()
    return render(request, 'plan_form.html', {'form': form, 'action': 'Create'})


# UPDATE WORKOUT PLAN
@login_required
def plan_update(request, pk):
    plan = get_object_or_404(WorkoutPlan, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workout plan updated!')
            return redirect('plan_list')
    else:
        form = WorkoutPlanForm(instance=plan)
    return render(request, 'plan_form.html', {'form': form, 'action': 'Update'})


# DELETE WORKOUT PLAN
@login_required
def plan_delete(request, pk):
    plan = get_object_or_404(WorkoutPlan, pk=pk, user=request.user)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Workout plan deleted!')
        return redirect('plan_list')
    return render(request, 'plan_confirm_delete.html', {'plan': plan})


# LOG WORKOUT
@login_required
def log_workout(request):
    if request.method == 'POST':
        form = WorkoutLogForm(request.POST, user=request.user)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, 'Workout logged!')
            return redirect('dashboard')
    else:
        form = WorkoutLogForm(user=request.user)
    return render(request, 'log_workout.html', {'form': form})
