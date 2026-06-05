from django.contrib import admin
from .models import CandidateProfile, EmployerProfile, JobPosting

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'years_of_experience', 'preferred_work_mode', 'is_member']
    search_fields = ['user__username', 'user__email', 'skills', 'location']
    list_filter = ['preferred_work_mode', 'is_member']

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'location', 'is_member']
    search_fields = ['user__username', 'company_name']
    list_filter = ['is_member']

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company_info', 'location', 'work_mode', 'years_of_experience', 'is_active', 'created_at']
    search_fields = ['job_title', 'company_info', 'required_skills', 'location']
    list_filter = ['work_mode', 'is_active']