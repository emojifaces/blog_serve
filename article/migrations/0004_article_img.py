# Generated by Django 3.1.3 on 2020-11-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20201112_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='img',
            field=models.ImageField(default='article/default_img.jpg', upload_to='article'),
        ),
    ]
