# Generated by Django 3.1.5 on 2023-06-26 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20220630_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='max_grade',
            field=models.PositiveIntegerField(default=0, verbose_name='Maksimal bal'),
        ),
        migrations.AddField(
            model_name='contest',
            name='min_grade',
            field=models.PositiveIntegerField(default=0, verbose_name="O'tish bali"),
        ),
        # migrations.AddField(
        #     model_name='usertestresult',
        #     name='ip_address',
        #     field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Ip Adres'),
        # ),
        migrations.AlterField(
            model_name='usertestresult',
            name='contest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contest_result', to='main.contest', verbose_name='Test'),
        ),
    ]
