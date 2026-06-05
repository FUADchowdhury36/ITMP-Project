from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ITMPApp', '0003_candidateprofile_cv_jobapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('job_title', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('candidate', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='work_experiences',
                    to='ITMPApp.candidateprofile',
                )),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
    ]
