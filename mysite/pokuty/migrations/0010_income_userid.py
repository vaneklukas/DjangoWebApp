# Generated by Django 3.0.6 on 2020-10-18 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokuty', '0009_auto_20201018_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='userID',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]