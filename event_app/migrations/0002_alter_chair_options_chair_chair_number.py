# Generated by Django 5.0.1 on 2024-02-02 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chair',
            options={'ordering': ['pk']},
        ),
        migrations.AddField(
            model_name='chair',
            name='chair_number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
