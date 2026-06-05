"""
ITMP Test Data Generator
Run with: python manage.py shell < ITMPApp/scripts/generate_data.py
Or copy-paste into: python manage.py shell
"""

from django.contrib.auth.models import User
from ITMPApp.models import CandidateProfile, EmployerProfile, JobPosting

# ─────────────────────────────────────────
# CLEAR EXISTING TEST DATA (optional)
# ─────────────────────────────────────────
print("Clearing old test data...")
User.objects.filter(username__startswith='candidate_').delete()
User.objects.filter(username__startswith='employer_').delete()

# ─────────────────────────────────────────
# CANDIDATES
# ─────────────────────────────────────────
candidates_data = [
    {
        'first_name': 'Alice', 'last_name': 'Johnson',
        'email': 'alice.johnson@email.com',
        'phone': '+61 412 345 678', 'location': 'Sydney, NSW',
        'university': 'University of Sydney', 'degree': 'Bachelor of Computer Science',
        'major': 'Software Engineering', 'graduation_year': '2022',
        'years_of_experience': 3, 'preferred_industry': 'Technology',
        'professional_summary': 'Passionate frontend developer with 3 years of experience building responsive web apps.',
        'skills': 'React, JavaScript, HTML, CSS, TypeScript, Figma',
        'preferred_work_mode': 'hybrid', 'preferred_location': 'Sydney, NSW',
        'is_member': True,
    },
    {
        'first_name': 'Ben', 'last_name': 'Williams',
        'email': 'ben.williams@email.com',
        'phone': '+61 423 456 789', 'location': 'Melbourne, VIC',
        'university': 'University of Melbourne', 'degree': 'Bachelor of Information Technology',
        'major': 'Cybersecurity', 'graduation_year': '2021',
        'years_of_experience': 4, 'preferred_industry': 'Finance',
        'professional_summary': 'Backend engineer specialising in Node.js and cloud infrastructure.',
        'skills': 'Node.js, Python, PostgreSQL, AWS, Docker, Kubernetes',
        'preferred_work_mode': 'remote', 'preferred_location': 'Melbourne, VIC',
        'is_member': False,
    },
    {
        'first_name': 'Cindy', 'last_name': 'Chen',
        'email': 'cindy.chen@email.com',
        'phone': '+61 434 567 890', 'location': 'Sydney, NSW',
        'university': 'UNSW Sydney', 'degree': 'Bachelor of Data Science',
        'major': 'Machine Learning', 'graduation_year': '2023',
        'years_of_experience': 2, 'preferred_industry': 'Technology',
        'professional_summary': 'Data analyst with strong Python and SQL skills, passionate about turning data into insights.',
        'skills': 'Python, SQL, Tableau, Excel, Machine Learning, Pandas',
        'preferred_work_mode': 'hybrid', 'preferred_location': 'Sydney, NSW',
        'is_member': True,
    },
    {
        'first_name': 'David', 'last_name': 'Nguyen',
        'email': 'david.nguyen@email.com',
        'phone': '+61 445 678 901', 'location': 'Brisbane, QLD',
        'university': 'Queensland University of Technology', 'degree': 'Bachelor of Engineering',
        'major': 'Software Engineering', 'graduation_year': '2020',
        'years_of_experience': 5, 'preferred_industry': 'Technology',
        'professional_summary': 'Full stack developer with expertise in React and Django.',
        'skills': 'React, Django, Python, JavaScript, PostgreSQL, REST API',
        'preferred_work_mode': 'onsite', 'preferred_location': 'Brisbane, QLD',
        'is_member': False,
    },
    {
        'first_name': 'Emma', 'last_name': 'Smith',
        'email': 'emma.smith@email.com',
        'phone': '+61 456 789 012', 'location': 'Perth, WA',
        'university': 'University of Western Australia', 'degree': 'Bachelor of Commerce',
        'major': 'Business Analytics', 'graduation_year': '2022',
        'years_of_experience': 2, 'preferred_industry': 'Consulting',
        'professional_summary': 'Business analyst with experience in process improvement and data reporting.',
        'skills': 'Excel, Power BI, SQL, Project Management, Communication',
        'preferred_work_mode': 'hybrid', 'preferred_location': 'Perth, WA',
        'is_member': False,
    },
    {
        'first_name': 'Frank', 'last_name': 'Lee',
        'email': 'frank.lee@email.com',
        'phone': '+61 467 890 123', 'location': 'Sydney, NSW',
        'university': 'University of Technology Sydney', 'degree': 'Master of Cybersecurity',
        'major': 'Network Security', 'graduation_year': '2021',
        'years_of_experience': 4, 'preferred_industry': 'Government',
        'professional_summary': 'Cybersecurity specialist with hands-on experience in penetration testing and security audits.',
        'skills': 'Python, Cybersecurity, Penetration Testing, Linux, Network Security, SIEM',
        'preferred_work_mode': 'onsite', 'preferred_location': 'Sydney, NSW',
        'is_member': True,
    },
    {
        'first_name': 'Grace', 'last_name': 'Kim',
        'email': 'grace.kim@email.com',
        'phone': '+61 478 901 234', 'location': 'Melbourne, VIC',
        'university': 'Monash University', 'degree': 'Bachelor of Computer Science',
        'major': 'Artificial Intelligence', 'graduation_year': '2023',
        'years_of_experience': 1, 'preferred_industry': 'Technology',
        'professional_summary': 'Fresh graduate with strong ML and Python skills looking for an entry-level AI role.',
        'skills': 'Python, Machine Learning, TensorFlow, PyTorch, SQL, Java',
        'preferred_work_mode': 'remote', 'preferred_location': 'Melbourne, VIC',
        'is_member': False,
    },
    {
        'first_name': 'Henry', 'last_name': 'Patel',
        'email': 'henry.patel@email.com',
        'phone': '+61 489 012 345', 'location': 'Adelaide, SA',
        'university': 'University of Adelaide', 'degree': 'Bachelor of Software Engineering',
        'major': 'Mobile Development', 'graduation_year': '2021',
        'years_of_experience': 3, 'preferred_industry': 'Technology',
        'professional_summary': 'Mobile developer experienced in React Native and Flutter.',
        'skills': 'React Native, Flutter, JavaScript, Swift, Kotlin, Firebase',
        'preferred_work_mode': 'hybrid', 'preferred_location': 'Adelaide, SA',
        'is_member': False,
    },
    {
        'first_name': 'Isla', 'last_name': 'Brown',
        'email': 'isla.brown@email.com',
        'phone': '+61 490 123 456', 'location': 'Sydney, NSW',
        'university': 'Macquarie University', 'degree': 'Bachelor of Information Systems',
        'major': 'Cloud Computing', 'graduation_year': '2022',
        'years_of_experience': 2, 'preferred_industry': 'Technology',
        'professional_summary': 'Cloud engineer with AWS and Azure certifications.',
        'skills': 'AWS, Azure, Docker, Kubernetes, Python, Terraform',
        'preferred_work_mode': 'remote', 'preferred_location': 'Sydney, NSW',
        'is_member': True,
    },
    {
        'first_name': 'James', 'last_name': 'Wilson',
        'email': 'james.wilson@email.com',
        'phone': '+61 401 234 567', 'location': 'Melbourne, VIC',
        'university': 'RMIT University', 'degree': 'Bachelor of Computer Science',
        'major': 'Game Development', 'graduation_year': '2020',
        'years_of_experience': 5, 'preferred_industry': 'Entertainment',
        'professional_summary': 'Senior software engineer with 5 years of experience in game development and C++.',
        'skills': 'C++, Unity, Unreal Engine, Python, Java, OpenGL',
        'preferred_work_mode': 'onsite', 'preferred_location': 'Melbourne, VIC',
        'is_member': False,
    },
]

print("Creating candidates...")
for i, data in enumerate(candidates_data):
    username = f"candidate_{data['email'].split('@')[0]}"
    user = User.objects.create_user(
        username=username,
        email=data['email'],
        password='testpass123',
        first_name=data['first_name'],
        last_name=data['last_name'],
    )
    CandidateProfile.objects.create(
        user=user,
        phone=data['phone'],
        location=data['location'],
        university=data['university'],
        degree=data['degree'],
        major=data['major'],
        graduation_year=data['graduation_year'],
        years_of_experience=data['years_of_experience'],
        preferred_industry=data['preferred_industry'],
        professional_summary=data['professional_summary'],
        skills=data['skills'],
        preferred_work_mode=data['preferred_work_mode'],
        preferred_location=data['preferred_location'],
        is_member=data['is_member'],
    )
    print(f"  ✅ Created candidate: {data['first_name']} {data['last_name']}")

# ─────────────────────────────────────────
# EMPLOYERS + JOB POSTINGS
# ─────────────────────────────────────────
employers_data = [
    {
        'first_name': 'Sarah', 'last_name': 'Thompson',
        'email': 'sarah@technovasolutions.com',
        'company_name': 'TechNova Solutions',
        'company_description': 'Leading software development company in Australia.',
        'location': 'Sydney, NSW',
        'is_member': True,
        'jobs': [
            {
                'job_title': 'Frontend Developer',
                'company_info': 'TechNova Solutions',
                'job_description': 'We are looking for a talented frontend developer to join our growing team. You will be responsible for building and maintaining high-quality web applications using React and TypeScript.',
                'required_education': "Bachelor's Degree in Computer Science or related field",
                'required_skills': 'React, JavaScript, TypeScript, HTML, CSS, Figma',
                'years_of_experience': 2,
                'work_mode': 'hybrid',
                'location': 'Sydney, NSW',
            },
            {
                'job_title': 'Senior Full Stack Developer',
                'company_info': 'TechNova Solutions',
                'job_description': 'Join our senior engineering team to build scalable web applications. You will work across the full stack using React and Django.',
                'required_education': "Bachelor's Degree in Software Engineering",
                'required_skills': 'React, Django, Python, PostgreSQL, REST API, Docker',
                'years_of_experience': 4,
                'work_mode': 'hybrid',
                'location': 'Sydney, NSW',
            },
        ]
    },
    {
        'first_name': 'Michael', 'last_name': 'Roberts',
        'email': 'michael@insightworks.com',
        'company_name': 'InsightWorks',
        'company_description': 'Data analytics and business intelligence consulting firm.',
        'location': 'Melbourne, VIC',
        'is_member': False,
        'jobs': [
            {
                'job_title': 'Data Analyst',
                'company_info': 'InsightWorks',
                'job_description': 'We are seeking a data analyst to help our clients make data-driven decisions. You will work with large datasets and create visualisations using Tableau and Power BI.',
                'required_education': "Bachelor's Degree in Data Science or Statistics",
                'required_skills': 'Python, SQL, Tableau, Excel, Power BI, Pandas',
                'years_of_experience': 2,
                'work_mode': 'remote',
                'location': 'Melbourne, VIC',
            },
            {
                'job_title': 'Machine Learning Engineer',
                'company_info': 'InsightWorks',
                'job_description': 'Join our AI team to build cutting-edge machine learning models for our enterprise clients.',
                'required_education': "Master's Degree in Computer Science or Data Science",
                'required_skills': 'Python, Machine Learning, TensorFlow, PyTorch, SQL',
                'years_of_experience': 3,
                'work_mode': 'hybrid',
                'location': 'Melbourne, VIC',
            },
        ]
    },
    {
        'first_name': 'Lisa', 'last_name': 'Anderson',
        'email': 'lisa@futurepathconsulting.com',
        'company_name': 'FuturePath Consulting',
        'company_description': 'Management and technology consulting for enterprise clients.',
        'location': 'Brisbane, QLD',
        'is_member': True,
        'jobs': [
            {
                'job_title': 'Business Analyst',
                'company_info': 'FuturePath Consulting',
                'job_description': 'We are looking for a business analyst to bridge the gap between business needs and technical solutions. You will work with stakeholders to document requirements and improve processes.',
                'required_education': "Bachelor's Degree in Business or IT",
                'required_skills': 'Excel, SQL, Communication, Project Management, Power BI',
                'years_of_experience': 2,
                'work_mode': 'onsite',
                'location': 'Brisbane, QLD',
            },
        ]
    },
    {
        'first_name': 'Tom', 'last_name': 'Garcia',
        'email': 'tom@cloudbridgetech.com',
        'company_name': 'CloudBridge Tech',
        'company_description': 'Cloud infrastructure and DevOps solutions provider.',
        'location': 'Sydney, NSW',
        'is_member': True,
        'jobs': [
            {
                'job_title': 'Cloud Engineer',
                'company_info': 'CloudBridge Tech',
                'job_description': 'Join our cloud team to design and maintain scalable infrastructure on AWS and Azure. You will work with Docker, Kubernetes, and Terraform.',
                'required_education': "Bachelor's Degree in Computer Science or Engineering",
                'required_skills': 'AWS, Azure, Docker, Kubernetes, Terraform, Python',
                'years_of_experience': 2,
                'work_mode': 'remote',
                'location': 'Sydney, NSW',
            },
            {
                'job_title': 'DevOps Engineer',
                'company_info': 'CloudBridge Tech',
                'job_description': 'We need a DevOps engineer to streamline our CI/CD pipelines and improve deployment processes.',
                'required_education': "Bachelor's Degree in IT or Software Engineering",
                'required_skills': 'Docker, Kubernetes, AWS, Python, Linux, Jenkins',
                'years_of_experience': 3,
                'work_mode': 'hybrid',
                'location': 'Sydney, NSW',
            },
        ]
    },
    {
        'first_name': 'Rachel', 'last_name': 'Martinez',
        'email': 'rachel@securenetsystems.com',
        'company_name': 'SecureNet Systems',
        'company_description': 'Cybersecurity solutions for government and enterprise.',
        'location': 'Canberra, ACT',
        'is_member': False,
        'jobs': [
            {
                'job_title': 'Cybersecurity Analyst',
                'company_info': 'SecureNet Systems',
                'job_description': 'We are seeking a cybersecurity analyst to protect our clients from digital threats. You will conduct security audits, penetration testing, and incident response.',
                'required_education': "Bachelor's Degree in Cybersecurity or Computer Science",
                'required_skills': 'Python, Cybersecurity, Penetration Testing, Linux, Network Security',
                'years_of_experience': 3,
                'work_mode': 'onsite',
                'location': 'Canberra, ACT',
            },
        ]
    },
]

print("\nCreating employers and job postings...")
for data in employers_data:
    username = f"employer_{data['email'].split('@')[0]}"
    user = User.objects.create_user(
        username=username,
        email=data['email'],
        password='testpass123',
        first_name=data['first_name'],
        last_name=data['last_name'],
    )
    EmployerProfile.objects.create(
        user=user,
        company_name=data['company_name'],
        company_description=data['company_description'],
        location=data['location'],
        is_member=data['is_member'],
    )
    print(f"  ✅ Created employer: {data['company_name']}")

    for job in data['jobs']:
        JobPosting.objects.create(
            employer=user,
            job_title=job['job_title'],
            company_info=job['company_info'],
            job_description=job['job_description'],
            required_education=job['required_education'],
            required_skills=job['required_skills'],
            years_of_experience=job['years_of_experience'],
            work_mode=job['work_mode'],
            location=job['location'],
            is_active=True,
        )
        print(f"     📋 Posted job: {job['job_title']}")

print("\n✅ ALL DONE! Here's your test data summary:")
print(f"   👤 Candidates created: {len(candidates_data)}")
print(f"   🏢 Employers created:  {len(employers_data)}")
total_jobs = sum(len(e['jobs']) for e in employers_data)
print(f"   💼 Jobs posted:        {total_jobs}")
print("\n🔑 All test accounts use password: testpass123")
print("\nSample logins:")
print("  Candidate: alice.johnson@email.com / testpass123")
print("  Employer:  sarah@technovasolutions.com / testpass123")
