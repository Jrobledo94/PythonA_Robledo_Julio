# Generated by Django 4.2.4 on 2023-08-17 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguimiento_ciudadano', '0007_alter_solicitudes_lat_alter_solicitudes_long'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitudes_api',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=1500)),
                ('request_id', models.CharField(max_length=100)),
                ('street_address', models.CharField(max_length=500)),
                ('apt_number', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(default='US', max_length=50)),
                ('zip_code', models.IntegerField()),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('solicitud_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(max_length=20)),
                ('media_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('agency_responsible', models.CharField(blank=True, max_length=100, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['request_id'],
            },
        ),
    ]
