# Generated by Django 4.2.14 on 2024-08-26 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0013_booking_razorpay_order_id_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="booking",
            unique_together={("time_slot", "booked_day", "patient")},
        ),
    ]
