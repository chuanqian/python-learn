# Generated by Django 2.2.15 on 2020-08-11 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='年龄'),
        ),
    ]
