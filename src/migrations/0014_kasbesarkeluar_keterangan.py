# Generated by Django 3.2.9 on 2022-10-05 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0013_auto_20221005_0342'),
    ]

    operations = [
        migrations.AddField(
            model_name='kasbesarkeluar',
            name='keterangan',
            field=models.TextField(blank=True, null=True),
        ),
    ]