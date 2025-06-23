from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('welcome/', views.home, name='home'),
    path('<int:major_id>/', views.major_detail, name='Major_detail'),
    path('subject_detail/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('cgpa-calculator/', views.cgpa_calculator, name='cgpa_calculator'),
    path('telegram-community/', views.telegram_community, name='telegram_community'),
    path('subjects/<int:subject_id>/pyqs/', views.subject_pyqs, name='subject_pyqs'),
    path('subjects/', views.subject_search, name='subject_search'),
    path('events/', views.events_page, name='events_page'),

]
