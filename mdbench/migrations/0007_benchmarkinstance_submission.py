# Generated by Django 3.2.7 on 2021-10-07 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdbench', '0006_auto_20211007_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='benchmarkinstance',
            name='submission',
            field=models.TextField(default='#SBATCH'),
            preserve_default=False,
        ),
    ]
