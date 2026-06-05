import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ITMPApp', '0002_jobposting_salary_max_jobposting_salary_min'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateprofile',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='cvs/'),
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ITMPApp.candidateprofile')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ITMPApp.jobposting')),
            ],
            options={
                'unique_together': {('candidate', 'job')},
            },
        ),
    ]
