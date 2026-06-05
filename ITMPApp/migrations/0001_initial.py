import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('university', models.CharField(blank=True, max_length=200)),
                ('degree', models.CharField(blank=True, max_length=200)),
                ('major', models.CharField(blank=True, max_length=200)),
                ('graduation_year', models.CharField(blank=True, max_length=10)),
                ('years_of_experience', models.IntegerField(default=0)),
                ('preferred_industry', models.CharField(blank=True, max_length=200)),
                ('professional_summary', models.TextField(blank=True)),
                ('skills', models.TextField(blank=True, help_text='Comma-separated skills e.g. Python, React')),
                ('preferred_work_mode', models.CharField(blank=True, choices=[('remote', 'Remote'), ('onsite', 'On-site'), ('hybrid', 'Hybrid')], max_length=10)),
                ('preferred_location', models.CharField(blank=True, max_length=100)),
                ('is_member', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=200)),
                ('company_description', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('website', models.URLField(blank=True)),
                ('is_member', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=200)),
                ('company_info', models.CharField(max_length=200)),
                ('job_description', models.TextField()),
                ('required_education', models.CharField(blank=True, max_length=200)),
                ('required_skills', models.TextField(blank=True, help_text='Comma-separated skills')),
                ('years_of_experience', models.IntegerField(default=0)),
                ('work_mode', models.CharField(choices=[('remote', 'Remote'), ('onsite', 'On-site'), ('hybrid', 'Hybrid')], max_length=10)),
                ('location', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
