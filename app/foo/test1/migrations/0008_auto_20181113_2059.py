# Generated by Django 2.1 on 2018-11-13 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0007_auto_20181107_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='user_name',
            field=models.CharField(default='abcdef', max_length=32, unique=True),
        ),
    ]
