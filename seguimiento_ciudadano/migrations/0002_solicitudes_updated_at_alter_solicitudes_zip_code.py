# Generated by Django 4.2.2 on 2023-08-16 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguimiento_ciudadano', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudes',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='solicitudes',
            name='zip_code',
            field=models.IntegerField(),
        ),
    ]