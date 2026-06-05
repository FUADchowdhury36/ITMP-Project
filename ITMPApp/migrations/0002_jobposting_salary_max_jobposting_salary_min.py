from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ITMPApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobposting',
            name='salary_max',
            field=models.IntegerField(blank=True, help_text='Maximum salary (AUD)', null=True),
        ),
        migrations.AddField(
            model_name='jobposting',
            name='salary_min',
            field=models.IntegerField(blank=True, help_text='Minimum salary (AUD)', null=True),
        ),
    ]
