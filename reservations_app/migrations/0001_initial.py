# Generated by Django 4.0.3 on 2022-03-18 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255)),
                ('capacity', models.PositiveSmallIntegerField()),
                ('projector', models.BooleanField(default=True)),
            ],
        ),
    ]
