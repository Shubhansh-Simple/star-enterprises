# Generated by Django 4.2 on 2024-03-21 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='entry_date',
            field=models.DateField(auto_now_add=True, unique=True),
        ),
    ]
