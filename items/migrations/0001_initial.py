# Generated by Django 4.2 on 2024-03-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Item Name', max_length=70, verbose_name='Item Name')),
                ('price', models.PositiveSmallIntegerField(verbose_name='Item Price')),
                ('total_quantity', models.SmallIntegerField(default=0, verbose_name='Total quantity of Item')),
                ('is_active', models.BooleanField(default=True, verbose_name='Status of Item')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
