# Generated by Django 3.2.8 on 2021-11-05 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdbench', '0013_auto_20211104_0311'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='label',
            field=models.CharField(default=1110, max_length=100),
            preserve_default=False,
        ),
    ]
