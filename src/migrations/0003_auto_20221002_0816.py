# Generated by Django 3.2.9 on 2022-10-02 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_auto_20221002_0807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lembaga',
            name='hp_pic',
        ),
        migrations.RemoveField(
            model_name='lembaga',
            name='nama_pic',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='hp_pic',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='nama_pic',
        ),
        migrations.AddField(
            model_name='lembaga',
            name='pic',
            field=models.CharField(default=False, max_length=255, verbose_name='Pic'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='pic',
            field=models.CharField(default=False, max_length=255, verbose_name='Pic'),
        ),
    ]
