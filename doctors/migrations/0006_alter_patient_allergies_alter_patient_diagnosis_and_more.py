# Generated by Django 4.2.14 on 2024-08-23 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0005_booking_patient"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="allergies",
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="diagnosis",
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="height",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=3, null=True
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="symptoms",
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="weight",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=3, null=True
            ),
        ),
    ]
