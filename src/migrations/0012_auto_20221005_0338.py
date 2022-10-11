# Generated by Django 3.2.9 on 2022-10-05 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0011_alter_kasbesar_keterangan'),
    ]

    operations = [
        migrations.CreateModel(
            name='KasBesarMasuk',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tgl_pencatatan', models.DateTimeField(blank=True, null=True)),
                ('no_transaksi', models.CharField(max_length=20)),
                ('pengirim', models.CharField(max_length=191)),
                ('bank_pengirim', models.CharField(max_length=191)),
                ('nominal', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_created_kasbesar_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_updated_kasbesar_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Kas Besar Masuk',
            },
        ),
        migrations.DeleteModel(
            name='KasBesar',
        ),
    ]