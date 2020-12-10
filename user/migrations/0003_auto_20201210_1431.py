# Generated by Django 3.1.3 on 2020-12-10 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.SmallIntegerField(choices=[(0, '女'), (1, '男'), (2, '保密')], default=2),
        ),
    ]
