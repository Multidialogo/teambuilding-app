# Generated by Django 4.0.1 on 2022-02-04 22:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import teambuilding.site.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('nickname', models.CharField(max_length=100, unique=True, verbose_name='nickname')),
                ('birth_date', models.DateField(help_text='Format: dd/mm/YYYY', verbose_name='birth date')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', teambuilding.site.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='account')),
            ],
            options={
                'verbose_name': 'user profile',
                'verbose_name_plural': 'user profiles',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=80, verbose_name='subject')),
                ('body', models.TextField(max_length=256, verbose_name='body')),
                ('read', models.BooleanField(default=False, verbose_name='read')),
                ('send_email', models.BooleanField(default=False, verbose_name='also send email')),
                ('origin', models.CharField(default='SYSTEM', editable=False, max_length=50, verbose_name='origin')),
                ('origin_object_id', models.CharField(blank=True, editable=False, max_length=64, null=True, verbose_name='origin object id')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site.userprofile', verbose_name='recipient')),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='HappyBirthdayMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('message', models.TextField(max_length=500, verbose_name='body')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='site.userprofile', verbose_name='recipient')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='site.userprofile', verbose_name='sender')),
            ],
            options={
                'verbose_name': 'happy birthday message',
                'verbose_name_plural': 'happy birthday messages',
                'ordering': ['created_at', 'recipient', 'sender'],
                'unique_together': {('created_at', 'recipient', 'sender')},
            },
        ),
    ]
