# Generated by Django 3.2.7 on 2021-10-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdbench', '0009_auto_20211007_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='software',
            name='toolchain_version',
            field=models.CharField(default='2020a', help_text='Enter a toolchain version', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='software',
            name='toolchain',
            field=models.CharField(help_text='Enter a toolchain name', max_length=100),
        ),
    ]
