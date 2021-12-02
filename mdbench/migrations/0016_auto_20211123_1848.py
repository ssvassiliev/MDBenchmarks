# Generated by Django 3.2.8 on 2021-11-23 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdbench', '0015_benchmark_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='serialbenchmarkinstance',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='benchmark',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]