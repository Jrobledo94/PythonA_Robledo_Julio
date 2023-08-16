# Generated by Django 4.2.4 on 2023-08-15 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitudes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=600)),
                ('request_id', models.CharField(max_length=100)),
                ('street_address', models.CharField(max_length=500)),
                ('apt_number', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
                ('zip_code', models.IntegerField(max_length=100)),
                ('lat', models.IntegerField()),
                ('long', models.IntegerField()),
                ('solicitud_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(max_length=20)),
                ('media_url', models.CharField(blank=True, max_length=500, null=True)),
                ('agency_responsible', models.CharField(blank=True, max_length=100, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['request_id'],
            },
        ),
    ]