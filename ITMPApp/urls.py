from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Candidate
    path('jobs/', views.job_search, name='job_search'),
    path('profile/', views.candidate_profile, name='candidate_profile'),
    path('profile/experience/add/', views.add_work_experience, name='add_work_experience'),
    path('profile/experience/<int:exp_id>/delete/', views.delete_work_experience, name='delete_work_experience'),

    # Employer
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('recommendations/', views.job_recommendations, name='job_recommendations'),
    path('candidates/recommended/', views.candidate_recommendations, name='candidate_recommendations'),
    path('membership/', views.membership_view, name='membership'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),

    path('candidates/search/', views.employer_candidate_search, name='employer_candidate_search'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('candidates/<int:candidate_id>/', views.candidate_detail, name='candidate_detail'),
]
