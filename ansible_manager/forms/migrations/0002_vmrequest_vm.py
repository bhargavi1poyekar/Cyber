# Generated by Django 4.2.3 on 2023-07-28 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VMRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_number', models.CharField(max_length=200)),
                ('course_name', models.CharField(max_length=200)),
                ('instructor_name', models.CharField(max_length=200)),
                ('ta_name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('semester', models.CharField(max_length=200)),
                ('year', models.PositiveSmallIntegerField()),
                ('os', models.CharField(max_length=200)),
                ('cpu_count', models.PositiveSmallIntegerField()),
                ('ram', models.PositiveSmallIntegerField()),
                ('ram_reason', models.TextField()),
                ('hard_disk', models.PositiveSmallIntegerField()),
                ('disk_reason', models.TextField()),
                ('num_vm', models.PositiveSmallIntegerField()),
                ('start_date', models.CharField(max_length=200)),
                ('end_date', models.CharField(max_length=200)),
                ('self_sudo', models.CharField(max_length=200)),
                ('vm_users', models.TextField()),
                ('vm_user_file', models.FileField(upload_to='vm_users/')),
                ('status', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_addr', models.CharField(max_length=200)),
                ('vm_name', models.CharField(max_length=200)),
                ('os', models.CharField(max_length=200)),
                ('template', models.CharField(max_length=200)),
                ('vmrequest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forms.vmrequest')),
            ],
        ),
    ]
