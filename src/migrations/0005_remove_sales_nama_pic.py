# Generated by Django 3.2.9 on 2022-10-02 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0004_auto_20221002_0816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='nama_pic',
        ),
    ]
