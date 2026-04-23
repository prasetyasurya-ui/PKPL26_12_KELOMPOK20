from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='LoginAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('ip_address', models.GenericIPAddressField()),
                ('failed_attempts', models.PositiveSmallIntegerField(default=0)),
                ('locked_until', models.DateTimeField(blank=True, null=True)),
                ('last_attempt_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('username', 'ip_address')},
            },
        ),
    ]
