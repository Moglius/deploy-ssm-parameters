# Generated by Django 4.2.5 on 2023-09-10 18:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ec2", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ec2server",
            name="operational",
            field=models.BooleanField(default=True),
        ),
    ]
