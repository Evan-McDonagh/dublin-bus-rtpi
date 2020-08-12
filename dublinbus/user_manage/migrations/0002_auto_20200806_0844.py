# Generated by Django 3.0.7 on 2020-08-06 07:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='male',
            new_name='gender',
        ),
        migrations.AddField(
            model_name='user',
            name='updatetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='regtime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]