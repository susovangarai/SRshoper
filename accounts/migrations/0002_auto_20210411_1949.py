# Generated by Django 3.2 on 2021-04-11 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210411_1949'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Gender',
        ),
    ]
