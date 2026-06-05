from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CandidateProfile, EmployerProfile, JobPosting

class UserRegistrationTest(TestCase):
    def test_candidate_registration(self):
        """Test that a candidate can register successfully"""
        response = self.client.post('/register/', {
            'fullname': 'Test Candidate',
            'email': 'candidate@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'role': 'candidate'
        })
        self.assertEqual(User.objects.filter(email='candidate@test.com').count(), 1)

    def test_employer_registration(self):
        """Test that an employer can register successfully"""
        response = self.client.post('/register/', {
            'fullname': 'Test Employer',
            'email': 'employer@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'role': 'employer'
        })
        self.assertEqual(User.objects.filter(email='employer@test.com').count(), 1)

    def test_password_mismatch(self):
        """Test that mismatched passwords are rejected"""
        self.client.post('/register/', {
            'fullname': 'Test User',
            'email': 'test@test.com',
            'password': 'testpass123',
            'confirm_password': 'wrongpassword',
            'role': 'candidate'
        })
        self.assertEqual(User.objects.filter(email='test@test.com').count(), 0)


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        CandidateProfile.objects.create(user=self.user)

    def test_login_valid(self):
        """Test that a valid user can log in"""
        response = self.client.post('/login/', {
            'email': 'test@test.com',
            'password': 'testpass123',
            'role': 'candidate'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid(self):
        """Test that wrong password is rejected"""
        response = self.client.post('/login/', {
            'email': 'test@test.com',
            'password': 'wrongpassword',
            'role': 'candidate'
        })
        self.assertEqual(response.status_code, 200)


class JobPostingTest(TestCase):
    def setUp(self):
        self.employer_user = User.objects.create_user(
            username='employer@test.com',
            email='employer@test.com',
            password='testpass123',
            first_name='Employer',
            last_name='Test'
        )
        EmployerProfile.objects.create(user=self.employer_user)

    def test_job_creation(self):
        """Test that an employer can create a job posting"""
        job = JobPosting.objects.create(
            employer=self.employer_user,
            job_title='Software Engineer',
            company_info='Test Company',
            job_description='Test description',
            required_skills='Python, Django',
            years_of_experience=2,
            work_mode='hybrid',
            location='Sydney, NSW'
        )
        self.assertEqual(JobPosting.objects.count(), 1)
        self.assertEqual(job.job_title, 'Software Engineer')

    def test_job_search(self):
        """Test that job search returns results"""
        JobPosting.objects.create(
            employer=self.employer_user,
            job_title='Python Developer',
            company_info='Test Company',
            job_description='Looking for Python developer',
            required_skills='Python, Django',
            years_of_experience=2,
            work_mode='remote',
            location='Melbourne, VIC'
        )
        self.client.login(username='employer@test.com', password='testpass123')
        self.assertEqual(JobPosting.objects.filter(job_title__icontains='Python').count(), 1)


class ModelTest(TestCase):
    def test_candidate_profile_creation(self):
        """Test CandidateProfile model"""
        user = User.objects.create_user(
            username='alice@test.com',
            email='alice@test.com',
            password='testpass123',
            first_name='Alice',
            last_name='Johnson'
        )
        profile = CandidateProfile.objects.create(
            user=user,
            skills='Python, Django, React',
            years_of_experience=3,
            preferred_work_mode='hybrid',
            location='Sydney, NSW'
        )
        self.assertEqual(profile.get_skills_list(), ['Python', 'Django', 'React'])
        self.assertEqual(profile.years_of_experience, 3)

    def test_home_page_loads(self):
        """Test that home page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)