# Generated by Django 4.2.6 on 2024-08-19 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materialTracker", "0011_alter_materialusage_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="worker",
            name="password",
            field=models.CharField(default="password", max_length=128),
        ),
    ]
