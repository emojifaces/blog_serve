# Generated by Django 3.1.3 on 2020-11-18 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_article_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(default='article/default_img.jpg', null=True, upload_to='article'),
        ),
    ]
