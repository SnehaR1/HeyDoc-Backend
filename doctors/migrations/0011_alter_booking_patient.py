# Generated by Django 4.2.14 on 2024-08-23 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0010_alter_patient_doctor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="doctors.patient",
                to_field="name",
            ),
        ),
    ]
