# Generated by Django 3.2.7 on 2021-10-20 13:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mdbench', '0009_resource_nnodes'),
    ]

    operations = [
        migrations.AddField(
            model_name='benchmarkinstance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='benchmarkinstance',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='serialbenchmarkinstance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serialbenchmarkinstance',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
