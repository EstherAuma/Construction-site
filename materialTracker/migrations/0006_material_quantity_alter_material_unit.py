# Generated by Django 4.2.2 on 2024-08-15 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materialTracker", "0005_alter_worker_email_alter_worker_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="material",
            name="quantity",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="material",
            name="unit",
            field=models.CharField(
                choices=[
                    ("m", "Meters"),
                    ("kg", "Kilograms"),
                    ("t", "Tons"),
                    ("L", "Liters"),
                    ("pcs", "Pieces"),
                ],
                default="kg",
                max_length=10,
            ),
        ),
    ]
