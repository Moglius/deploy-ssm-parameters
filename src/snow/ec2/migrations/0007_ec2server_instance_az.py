# Generated by Django 4.2.5 on 2023-09-17 17:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ec2", "0006_blockdevice_available_blockdevice_volume_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="ec2server",
            name="instance_az",
            field=models.CharField(blank=True, default="", max_length=30),
        ),
    ]
