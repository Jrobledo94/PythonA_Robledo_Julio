# Generated by Django 4.2.2 on 2023-08-21 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguimiento_ciudadano', '0002_alter_solicitudes_api_solicitud_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudes',
            name='solicitud_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]