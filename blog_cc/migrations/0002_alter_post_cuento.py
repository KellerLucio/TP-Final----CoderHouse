# Generated by Django 4.1.7 on 2023-04-22 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_cc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cuento',
            field=models.CharField(max_length=1000),
        ),
    ]