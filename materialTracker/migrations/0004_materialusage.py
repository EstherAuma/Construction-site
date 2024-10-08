# Generated by Django 5.1 on 2024-08-08 10:39

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materialTracker", "0003_material"),
    ]

    operations = [
        migrations.CreateModel(
            name="MaterialUsage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.CharField(max_length=10)),
                ("date_used", models.DateField(default=django.utils.timezone.now)),
                (
                    "price_per_unit",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="materialTracker.material",
                    ),
                ),
            ],
        ),
    ]
