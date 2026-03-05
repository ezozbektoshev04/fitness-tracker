from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('plans/', views.plan_list, name='plan_list'),
    path('plans/<int:pk>/', views.plan_detail, name='plan_detail'),
    path('plans/create/', views.plan_create, name='plan_create'),
    path('plans/<int:pk>/update/', views.plan_update, name='plan_update'),
    path('plans/<int:pk>/delete/', views.plan_delete, name='plan_delete'),
    path('log/', views.log_workout, name='log_workout'),
]
