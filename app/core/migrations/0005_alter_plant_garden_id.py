# Generated by Django 3.2.18 on 2023-02-22 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20230222_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='garden_id',
            field=models.IntegerField(max_length=255),
        ),
    ]
