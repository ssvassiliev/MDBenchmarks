# Generated by Django 3.2.7 on 2021-10-10 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdbench', '0005_alter_benchmarkinstance_cpu_efficiency'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimulationInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.TextField()),
                ('benchmark', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='mdbench.benchmark')),
                ('software', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='mdbench.software')),
            ],
            options={
                'verbose_name_plural': '5. Simulation input',
            },
        ),
    ]
