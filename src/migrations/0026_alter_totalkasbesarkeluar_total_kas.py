# Generated by Django 3.2.9 on 2022-10-12 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0025_alter_sales_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totalkasbesarkeluar',
            name='total_kas',
            field=models.FloatField(),
        ),
    ]