# Generated by Django 4.1.7 on 2023-04-22 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_cc', '0002_alter_post_cuento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post',
            field=models.CharField(max_length=120),
        ),
    ]
