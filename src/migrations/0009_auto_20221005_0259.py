# Generated by Django 3.2.9 on 2022-10-05 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0008_purchases_dp_persen'),
    ]

    operations = [
        migrations.AddField(
            model_name='kasbesar',
            name='jenis_kas',
            field=models.CharField(default='Keluar', max_length=20),
        ),
        migrations.AddField(
            model_name='kasbesar',
            name='keterangan',
            field=models.TextField(blank=True, null=True),
        ),
    ]
