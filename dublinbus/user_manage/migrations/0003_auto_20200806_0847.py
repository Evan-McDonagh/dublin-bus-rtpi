# Generated by Django 3.0.7 on 2020-08-06 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0002_auto_20200806_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=300),
        ),
    ]
