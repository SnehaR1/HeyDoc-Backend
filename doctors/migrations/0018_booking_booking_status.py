# Generated by Django 4.2.14 on 2024-08-29 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0017_remove_booking_razorpay_order_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="booking_status",
            field=models.CharField(
                choices=[("Booked", "Booked"), ("Cancelled", "Cancelled")],
                default="Booked",
            ),
        ),
    ]
