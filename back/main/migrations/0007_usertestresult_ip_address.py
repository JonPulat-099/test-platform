# Generated by Django 3.1.5 on 2023-09-24 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20230626_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertestresult',
            name='ip_address',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Ip Adres'),
        ),
    ]
