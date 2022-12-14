# Generated by Django 3.1.4 on 2022-08-18 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
            },
        ),
        migrations.CreateModel(
            name='VDCMunicipality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vdc_municipality', to='address.district')),
            ],
            options={
                'verbose_name': 'VDC/Municipality',
                'verbose_name_plural': 'VDC/Municipalities',
            },
        ),
        migrations.CreateModel(
            name='WardNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward_number', models.IntegerField(blank=True, null=True, verbose_name='Ward Number')),
                ('vdc_municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ward_number', to='address.vdcmunicipality', verbose_name='VDC/Municipality')),
            ],
            options={
                'verbose_name': 'Ward Number',
                'verbose_name_plural': 'Ward Numbers',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='province', to='address.country')),
            ],
            options={
                'verbose_name': 'Province',
                'verbose_name_plural': 'Provinces',
            },
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='district', to='address.province'),
        ),
        migrations.AddConstraint(
            model_name='wardnumber',
            constraint=models.UniqueConstraint(fields=('ward_number', 'vdc_municipality'), name='Unique Ward Number in a VDC/Municipality'),
        ),
        migrations.AddConstraint(
            model_name='vdcmunicipality',
            constraint=models.UniqueConstraint(fields=('name', 'district'), name='Unique VDC/Municipality in a District'),
        ),
        migrations.AddConstraint(
            model_name='province',
            constraint=models.UniqueConstraint(fields=('name', 'country'), name='Unique Province in a Country'),
        ),
        migrations.AddConstraint(
            model_name='district',
            constraint=models.UniqueConstraint(fields=('name', 'province'), name='Unique District in a Province'),
        ),
    ]
