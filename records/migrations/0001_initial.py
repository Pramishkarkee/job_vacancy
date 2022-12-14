# Generated by Django 3.1.4 on 2022-08-18 08:18

import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('professional', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('middle_name', models.CharField(blank=True, max_length=150, verbose_name='Middle Name')),
                ('contact_number', models.CharField(max_length=20, verbose_name='Contact Number')),
                ('profile_photo', models.ImageField(default='users/default.jpg', upload_to='users/profile-photo/', verbose_name='Profile Picture')),
                ('profile_type', models.CharField(choices=[('A', 'Applicant'), ('P', 'Provider'), ('S', 'Admin')], max_length=1)),
                ('is_registered', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='records.user')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('records.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.OneToOneField(limit_choices_to={'profile_type': 'P'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='provider', serialize=False, to='records.user', verbose_name='ID')),
                ('website', models.URLField(blank=True, max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='provider', to='address.wardnumber', verbose_name='Address')),
                ('categories_covered', models.ManyToManyField(related_name='provider', to='professional.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.OneToOneField(limit_choices_to={'profile_type': 'A'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='applicant', serialize=False, to='records.user', verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, verbose_name='Gender')),
                ('date_of_birth', models.DateField(verbose_name='Date of Birth')),
                ('cv', models.FileField(upload_to='users/cv', verbose_name='CV')),
                ('supporting_document', models.FileField(blank=True, help_text='Combine all your supporting documentsinto a single PDF file before uploading.', null=True, upload_to='users/supporting', verbose_name='Supporting Document')),
                ('profile_links', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, null=True, size=None, verbose_name='Links to Professional Profiles')),
                ('employment_status', models.CharField(choices=[('Unemployed', 'Unemployed'), ('Student', 'Student'), ('Part Time', 'Part Time'), ('Full Time', 'Full Time')], max_length=50)),
                ('experience', models.ManyToManyField(related_name='applicant', to='professional.Experience')),
                ('interested_categories', models.ManyToManyField(related_name='applicant_interested', to='professional.Category')),
                ('permanent_address', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='applicant_permanent', to='address.wardnumber', verbose_name='Permanent Address')),
                ('qualification', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='applicant', to='professional.qualification')),
                ('skills', models.ManyToManyField(related_name='applicant', to='professional.Skill')),
                ('temporary_address', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='applicant_temporary', to='address.wardnumber', verbose_name='Temporary Address')),
            ],
        ),
    ]
