# Generated by Django 3.1.5 on 2022-06-30 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='duration',
            field=models.PositiveIntegerField(default=60),
        ),
        migrations.AlterField(
            model_name='usertestresult',
            name='point',
            field=models.IntegerField(null=True, verbose_name='Umumiy ball'),
        ),
    ]