# Generated by Django 5.0.1 on 2024-09-06 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('like_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='likeitem',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
    ]
