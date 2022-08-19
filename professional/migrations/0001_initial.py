# Generated by Django 3.1.4 on 2022-08-18 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('desription', models.CharField(blank=True, max_length=500, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('no_of_years', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Experience',
                'verbose_name_plural': 'Experiences',
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('', '(Select Level)'), ("Bachelor's", "Bachelor's Degree"), ("Master's", "Master's Degree"), ('PhD', 'PhD')], max_length=10, verbose_name='Qualification Level')),
                ('field', models.CharField(max_length=100, verbose_name='Qualification Field')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Name of the skill')),
                ('description', models.CharField(blank=True, max_length=750, verbose_name='Description')),
            ],
        ),
        migrations.AddConstraint(
            model_name='experience',
            constraint=models.UniqueConstraint(fields=('role', 'no_of_years'), name='One entry for a number of year for a role'),
        ),
    ]
