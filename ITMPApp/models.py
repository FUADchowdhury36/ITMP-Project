from django.db import models
from django.contrib.auth.models import User


# Candidate Profile
class CandidateProfile(models.Model):
    WORK_MODE_CHOICES = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Education
    university = models.CharField(max_length=200, blank=True)
    degree = models.CharField(max_length=200, blank=True)
    major = models.CharField(max_length=200, blank=True)
    graduation_year = models.CharField(max_length=10, blank=True)

    # Experience
    years_of_experience = models.IntegerField(default=0)
    preferred_industry = models.CharField(max_length=200, blank=True)
    professional_summary = models.TextField(blank=True)

    # Skills & Preferences
    skills = models.TextField(blank=True, help_text="Comma-separated skills e.g. Python, React")
    preferred_work_mode = models.CharField(max_length=10, choices=WORK_MODE_CHOICES, blank=True)
    preferred_location = models.CharField(max_length=100, blank=True)

    # CV
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)

    # Membership
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} - Candidate"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]


# Work Experience (linked to CandidateProfile)
class WorkExperience(models.Model):
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name='work_experiences'
    )
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    def duration_display(self):
        """Return a human-readable duration string."""
        from datetime import date
        end = date.today() if self.is_current else self.end_date
        if not end:
            return "Present"
        months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
        years, remaining = divmod(months, 12)
        parts = []
        if years:
            parts.append(f"{years} yr{'s' if years > 1 else ''}")
        if remaining:
            parts.append(f"{remaining} mo")
        return " ".join(parts) if parts else "< 1 mo"


# Employer Profile
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, blank=True)
    company_description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    # Membership
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_name} - Employer"


# Job Posting
class JobPosting(models.Model):
    WORK_MODE_CHOICES = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]

    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    company_info = models.CharField(max_length=200)
    job_description = models.TextField()
    required_education = models.CharField(max_length=200, blank=True)
    required_skills = models.TextField(blank=True, help_text="Comma-separated skills")
    years_of_experience = models.IntegerField(default=0)
    work_mode = models.CharField(max_length=10, choices=WORK_MODE_CHOICES)
    location = models.CharField(max_length=200)
    salary_min = models.IntegerField(null=True, blank=True, help_text="Minimum salary (AUD)")
    salary_max = models.IntegerField(null=True, blank=True, help_text="Maximum salary (AUD)")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_info}"

    def get_skills_list(self):
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]


# Job Application — must be AFTER both CandidateProfile and JobPosting
class JobApplication(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f"{self.candidate.user.get_full_name()} → {self.job.job_title}"
