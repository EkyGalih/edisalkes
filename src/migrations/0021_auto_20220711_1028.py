# Generated by Django 3.2.9 on 2022-07-11 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0020_alter_sales_overdue'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchases',
            name='ongkos_kirim',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
