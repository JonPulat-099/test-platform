# Generated by Django 3.1.5 on 2023-06-26 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20230626_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='max_grade',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='min_grade',
        ),
        migrations.AddField(
            model_name='contest',
            name='grade_per_question',
            field=models.PositiveIntegerField(default=0, verbose_name='Bal'),
        ),
        # migrations.AddField(
        #     model_name='usertestresult',
        #     name='ip_address',
        #     field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Ip Adres'),
        # ),
    ]
