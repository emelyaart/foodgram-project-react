# Generated by Django 3.2.5 on 2021-07-08 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_ingredient_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='unit',
            new_name='measurement_unit',
        ),
    ]
