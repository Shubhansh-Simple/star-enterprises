# Generated by Django 4.2 on 2024-03-18 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_alter_items_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='items',
            old_name='total_quantity',
            new_name='quantity',
        ),
    ]
