# Generated by Django 4.2.14 on 2024-08-23 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0008_alter_patient_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="patient",
            name="doctor",
        ),
        migrations.AddField(
            model_name="patient",
            name="doctor",
            field=models.ManyToManyField(blank=True, null=True, to="doctors.doctor"),
        ),
    ]
