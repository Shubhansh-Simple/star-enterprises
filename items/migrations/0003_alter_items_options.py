# Generated by Django 4.2 on 2024-03-03 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_alter_items_options_alter_items_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='items',
            options={'ordering': ['name', 'is_active'], 'verbose_name': 'Item', 'verbose_name_plural': 'Items'},
        ),
    ]