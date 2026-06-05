from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CandidateProfile, EmployerProfile, JobPosting, JobApplication, WorkExperience
from django.db.models import Q
from django.shortcuts import get_object_or_404
from thefuzz import fuzz


# ─────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────
def home(request):
    if request.user.is_authenticated:
        try:
            CandidateProfile.objects.get(user=request.user)
            return redirect('candidate_dashboard')
        except CandidateProfile.DoesNotExist:
            return redirect('employer_dashboard')
    return render(request, 'ITMPApp/home.html')


# ─────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')  # 'candidate' or 'employer'

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'ITMPApp/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'ITMPApp/register.html')

        name_parts = full_name.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        if role == 'candidate':
            CandidateProfile.objects.create(user=user)
        else:
            EmployerProfile.objects.create(user=user)

        login(request, user)

        if role == 'candidate':
            return redirect('candidate_dashboard')
        else:
            return redirect('employer_dashboard')

    return render(request, 'ITMPApp/register.html')


# ─────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if role == 'candidate':
                return redirect('candidate_dashboard')
            else:
                return redirect('employer_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'ITMPApp/login.html')


# ─────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────
def logout_view(request):
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────
# JOB SEARCH (Candidate)
# ─────────────────────────────────────────
@login_required
def job_search(request):
    all_jobs = JobPosting.objects.filter(is_active=True)
    jobs = all_jobs

    keyword   = request.GET.get('keyword', '').strip()
    location  = request.GET.get('location', '').strip()
    work_mode = request.GET.get('work_mode', '').strip()
    experience = request.GET.get('experience', '').strip()
    salary    = request.GET.get('salary', '').strip()

    if location:
        jobs = jobs.filter(location__icontains=location)
    if work_mode:
        jobs = jobs.filter(work_mode=work_mode)
    if experience:
        jobs = jobs.filter(years_of_experience__lte=int(experience))
    if salary:
        try:
            salary_val = int(salary)
            jobs = jobs.filter(
                Q(salary_min__lte=salary_val) | Q(salary_min__isnull=True)
            ).filter(
                Q(salary_max__gte=salary_val) | Q(salary_max__isnull=True)
            )
        except ValueError:
            pass

    if keyword:
        fuzzy_matches = []
        for job in jobs:
            title_score  = fuzz.partial_ratio(keyword.lower(), job.job_title.lower())
            desc_score   = fuzz.partial_ratio(keyword.lower(), job.job_description.lower())
            skills_score = fuzz.partial_ratio(keyword.lower(), job.required_skills.lower())
            best_score = max(title_score, desc_score, skills_score)
            if best_score >= 65:
                fuzzy_matches.append(job)
        jobs = fuzzy_matches
    else:
        jobs = list(jobs)

    return render(request, 'ITMPApp/job_search.html', {
        'jobs': jobs,
        'keyword': keyword,
        'location': location,
        'work_mode': work_mode,
        'experience': experience,
        'salary': salary,
    })


# ─────────────────────────────────────────
# CANDIDATE PROFILE
# ─────────────────────────────────────────
@login_required
def candidate_profile(request):
    profile, created = CandidateProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name  = request.POST.get('last_name', '')
        request.user.email      = request.POST.get('email', '')
        request.user.save()

        profile.phone               = request.POST.get('phone', '')
        profile.location            = request.POST.get('location', '')
        profile.preferred_work_mode = request.POST.get('preferred_work_mode', '')
        profile.preferred_location  = request.POST.get('preferred_location', '')

        profile.university       = request.POST.get('university', '')
        profile.degree           = request.POST.get('degree', '')
        profile.major            = request.POST.get('major', '')
        profile.graduation_year  = request.POST.get('graduation_year', '')

        profile.years_of_experience  = request.POST.get('years_of_experience', 0)
        profile.preferred_industry   = request.POST.get('preferred_industry', '')
        profile.professional_summary = request.POST.get('professional_summary', '')

        profile.skills = request.POST.get('skills', '')

        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('candidate_profile')

    work_experiences = WorkExperience.objects.filter(candidate=profile)
    return render(request, 'ITMPApp/candidate_profile.html', {
        'profile': profile,
        'work_experiences': work_experiences,
    })


# ─────────────────────────────────────────
# WORK EXPERIENCE — ADD
# ─────────────────────────────────────────
@login_required
def add_work_experience(request):
    if request.method == 'POST':
        profile = get_object_or_404(CandidateProfile, user=request.user)

        company_name = request.POST.get('company_name', '').strip()
        job_title    = request.POST.get('job_title', '').strip()
        start_date   = request.POST.get('start_date', '').strip()
        end_date     = request.POST.get('end_date', '').strip() or None
        is_current   = request.POST.get('is_current') == 'on'
        description  = request.POST.get('description', '').strip()

        if company_name and job_title and start_date:
            WorkExperience.objects.create(
                candidate=profile,
                company_name=company_name,
                job_title=job_title,
                start_date=start_date,
                end_date=None if is_current else end_date,
                is_current=is_current,
                description=description,
            )
            messages.success(request, f'Work experience at {company_name} added.')
        else:
            messages.error(request, 'Company name, job title and start date are required.')

    return redirect('candidate_profile')


# ─────────────────────────────────────────
# WORK EXPERIENCE — DELETE
# ─────────────────────────────────────────
@login_required
def delete_work_experience(request, exp_id):
    profile = get_object_or_404(CandidateProfile, user=request.user)
    exp = get_object_or_404(WorkExperience, id=exp_id, candidate=profile)
    exp.delete()
    messages.success(request, 'Work experience removed.')
    return redirect('candidate_profile')


# ─────────────────────────────────────────
# EMPLOYER DASHBOARD
# ─────────────────────────────────────────
@login_required
def employer_dashboard(request):
    try:
        employer_profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        employer_profile = None

    my_jobs     = JobPosting.objects.filter(employer=request.user)
    total_jobs  = my_jobs.count()

    return render(request, 'ITMPApp/employer_dashboard.html', {
        'employer_profile': employer_profile,
        'my_jobs': my_jobs,
        'total_jobs': total_jobs,
    })


# ─────────────────────────────────────────
# CREATE JOB (Employer)
# ─────────────────────────────────────────
@login_required
def create_job(request):
    if request.method == 'POST':
        JobPosting.objects.create(
            employer=request.user,
            job_title=request.POST.get('job_title'),
            company_info=request.POST.get('company_info'),
            job_description=request.POST.get('job_description'),
            required_education=request.POST.get('required_education'),
            required_skills=request.POST.get('required_skills'),
            years_of_experience=request.POST.get('years_of_experience', 0),
            work_mode=request.POST.get('work_mode'),
            location=request.POST.get('location'),
        )
        messages.success(request, 'Job posted successfully!')
        return redirect('employer_dashboard')

    return render(request, 'ITMPApp/create_job.html')


# ─────────────────────────────────────────
# RECOMMENDATION ENGINE
# ─────────────────────────────────────────

def calculate_job_match_score(profile, job):
    """Score how well a job matches a candidate's profile."""
    score = 0

    if profile.skills and job.required_skills:
        candidate_skills = set(s.lower().strip() for s in profile.skills.split(','))
        job_skills       = set(s.lower().strip() for s in job.required_skills.split(','))
        score += len(candidate_skills.intersection(job_skills)) * 10

    if profile.preferred_work_mode and job.work_mode:
        if profile.preferred_work_mode == job.work_mode:
            score += 20

    candidate_loc = (profile.preferred_location or profile.location or '').lower().strip()
    if candidate_loc and job.location:
        if candidate_loc in job.location.lower() or job.location.lower() in candidate_loc:
            score += 15

    if profile.years_of_experience >= job.years_of_experience:
        score += 10

    return score


def calculate_candidate_match_score(job, profile):
    """Score how well a candidate matches a job posting."""
    score = 0

    if job.required_skills and profile.skills:
        job_skills       = set(s.lower().strip() for s in job.required_skills.split(','))
        candidate_skills = set(s.lower().strip() for s in profile.skills.split(','))
        score += len(job_skills.intersection(candidate_skills)) * 10

    if job.work_mode and profile.preferred_work_mode:
        if job.work_mode == profile.preferred_work_mode:
            score += 20

    if job.location and profile.location:
        if job.location.lower() in profile.location.lower() or \
           profile.location.lower() in job.location.lower():
            score += 15

    if profile.years_of_experience >= job.years_of_experience:
        score += 10

    return score


@login_required
def job_recommendations(request):
    """Show recommended jobs for a candidate."""
    try:
        profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return redirect('candidate_profile')

    all_jobs    = JobPosting.objects.filter(is_active=True)
    scored_jobs = []
    for job in all_jobs:
        score = calculate_job_match_score(profile, job)
        if score > 0:
            scored_jobs.append({'job': job, 'score': score})

    scored_jobs.sort(key=lambda x: x['score'], reverse=True)

    if not profile.is_member:
        scored_jobs = scored_jobs[:10]

    return render(request, 'ITMPApp/job_recommendations.html', {
        'scored_jobs': scored_jobs,
        'is_member': profile.is_member,
    })


@login_required
def candidate_recommendations(request):
    """Show recommended candidates for an employer's job."""
    job_id = request.GET.get('job_id')

    try:
        employer_profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return redirect('employer_dashboard')

    my_jobs      = JobPosting.objects.filter(employer=request.user, is_active=True)
    selected_job = None

    if job_id:
        try:
            selected_job = JobPosting.objects.get(id=job_id, employer=request.user)
        except JobPosting.DoesNotExist:
            pass

    if not selected_job and my_jobs.exists():
        selected_job = my_jobs.first()

    scored_candidates = []
    if selected_job:
        for candidate in CandidateProfile.objects.all():
            score = calculate_candidate_match_score(selected_job, candidate)
            if score > 0:
                scored_candidates.append({'candidate': candidate, 'score': score})

        scored_candidates.sort(key=lambda x: x['score'], reverse=True)

        if not employer_profile.is_member:
            scored_candidates = scored_candidates[:10]

    return render(request, 'ITMPApp/candidate_recommendations.html', {
        'scored_candidates': scored_candidates,
        'my_jobs': my_jobs,
        'selected_job': selected_job,
        'is_member': employer_profile.is_member,
    })


# ─────────────────────────────────────────
# MEMBERSHIP  (mock payment gate)
# ─────────────────────────────────────────
@login_required
def membership_view(request):
    # Resolve current user's profile
    profile = None
    try:
        profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        try:
            profile = EmployerProfile.objects.get(user=request.user)
        except EmployerProfile.DoesNotExist:
            pass

    if request.method == 'POST':
        card_number = request.POST.get('card_number', '').replace(' ', '').replace('-', '')
        card_name   = request.POST.get('card_name', '').strip()
        card_expiry = request.POST.get('card_expiry', '').strip()
        card_cvv    = request.POST.get('card_cvv', '').strip()

        # Simple mock validation
        errors = []
        if not card_name:
            errors.append('Cardholder name is required.')
        if len(card_number) != 16 or not card_number.isdigit():
            errors.append('Card number must be 16 digits.')
        if not card_expiry:
            errors.append('Expiry date is required.')
        if len(card_cvv) not in (3, 4) or not card_cvv.isdigit():
            errors.append('CVV must be 3 or 4 digits.')

        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, 'ITMPApp/membership.html', {
                'profile': profile,
                'card_name': card_name,
                'card_expiry': card_expiry,
            })

        # Activate membership
        if profile:
            profile.is_member = True
            profile.save()

        messages.success(request, 'Payment successful! Your Premium membership is now active.')
        return redirect(request.POST.get('next', 'home'))

    return render(request, 'ITMPApp/membership.html', {'profile': profile})


# ─────────────────────────────────────────
# EMPLOYER CANDIDATE SEARCH
# ─────────────────────────────────────────
@login_required
def employer_candidate_search(request):
    try:
        EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return redirect('employer_dashboard')

    all_candidates = CandidateProfile.objects.filter(
        user__first_name__isnull=False
    ).exclude(user__first_name='')
    candidates = all_candidates

    keyword    = request.GET.get('keyword', '').strip()
    location   = request.GET.get('location', '').strip()
    work_mode  = request.GET.get('work_mode', '').strip()
    experience = request.GET.get('experience', '').strip()
    education  = request.GET.get('education', '').strip()

    if location:
        candidates = candidates.filter(
            Q(location__icontains=location) |
            Q(preferred_location__icontains=location)
        )
    if work_mode:
        candidates = candidates.filter(preferred_work_mode=work_mode)
    if experience:
        try:
            candidates = candidates.filter(years_of_experience__gte=int(experience))
        except ValueError:
            pass
    if education:
        candidates = candidates.filter(
            Q(degree__icontains=education) |
            Q(major__icontains=education)
        )

    if keyword:
        fuzzy_matches = []
        for candidate in candidates:
            full_name     = candidate.user.get_full_name().lower()
            skills        = (candidate.skills or '').lower()
            summary       = (candidate.professional_summary or '').lower()
            major         = (candidate.major or '').lower()
            kw            = keyword.lower()

            best_score = max(
                fuzz.partial_ratio(kw, full_name),
                fuzz.partial_ratio(kw, skills),
                fuzz.partial_ratio(kw, summary),
                fuzz.partial_ratio(kw, major),
            )
            if best_score >= 65:
                fuzzy_matches.append(candidate)
        candidates = fuzzy_matches
    else:
        candidates = list(candidates)

    return render(request, 'ITMPApp/employer_candidate_search.html', {
        'candidates': candidates,
        'keyword':    keyword,
        'location':   location,
        'work_mode':  work_mode,
        'experience': experience,
        'education':  education,
        'total':      len(candidates),
    })


# ─────────────────────────────────────────
# CANDIDATE DASHBOARD
# ─────────────────────────────────────────
@login_required
def candidate_dashboard(request):
    try:
        profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return redirect('candidate_profile')

    fields_to_check = [
        request.user.first_name,
        request.user.last_name,
        profile.phone,
        profile.location,
        profile.preferred_location,
        profile.preferred_work_mode,
        profile.university,
        profile.degree,
        profile.major,
        profile.skills,
        profile.professional_summary,
    ]
    filled = sum(1 for f in fields_to_check if f and str(f).strip())
    profile_strength = int((filled / len(fields_to_check)) * 100)

    all_jobs    = JobPosting.objects.filter(is_active=True)
    scored_jobs = []
    for job in all_jobs:
        score = calculate_job_match_score(profile, job)
        if score > 0:
            scored_jobs.append({'job': job, 'score': score})
    scored_jobs.sort(key=lambda x: x['score'], reverse=True)
    top_jobs = scored_jobs[:3]

    total_jobs  = JobPosting.objects.filter(is_active=True).count()
    match_count = len(scored_jobs)

    return render(request, 'ITMPApp/candidate_dashboard.html', {
        'profile':          profile,
        'top_jobs':         top_jobs,
        'profile_strength': profile_strength,
        'total_jobs':       total_jobs,
        'match_count':      match_count,
    })


# ─────────────────────────────────────────
# JOB DETAIL
# ─────────────────────────────────────────
@login_required
def job_detail(request, job_id):
    try:
        job = JobPosting.objects.get(id=job_id, is_active=True)
    except JobPosting.DoesNotExist:
        return redirect('job_search')

    has_applied = False
    try:
        profile = CandidateProfile.objects.get(user=request.user)
        has_applied = JobApplication.objects.filter(candidate=profile, job=job).exists()
        if request.method == 'POST':
            if not has_applied:
                JobApplication.objects.create(candidate=profile, job=job)
                has_applied = True
                messages.success(request, 'Application submitted successfully!')
            else:
                messages.info(request, 'You have already applied for this job.')
    except CandidateProfile.DoesNotExist:
        pass

    return render(request, 'ITMPApp/job_detail.html', {
        'job': job,
        'has_applied': has_applied,
    })


# ─────────────────────────────────────────
# CANDIDATE DETAIL (Employer View)
# ─────────────────────────────────────────
@login_required
def candidate_detail(request, candidate_id):
    try:
        EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return redirect('employer_dashboard')

    try:
        candidate = CandidateProfile.objects.get(id=candidate_id)
    except CandidateProfile.DoesNotExist:
        return redirect('employer_candidate_search')

    work_experiences = WorkExperience.objects.filter(candidate=candidate)
    return render(request, 'ITMPApp/candidate_detail.html', {
        'candidate': candidate,
        'work_experiences': work_experiences,
    })
