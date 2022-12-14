# Generated by Django 3.2.9 on 2022-10-13 12:30

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group', models.IntegerField(choices=[(0, 'Belum Terdaftar'), (1, 'Super Admin'), (2, 'Admin')], default=0)),
                ('is_email_confirm', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, max_length=14, null=True)),
                ('nik', models.CharField(blank=True, max_length=16, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Beban',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('kode_beban', models.CharField(default=0, max_length=255, unique=True)),
                ('jenis_biaya', models.CharField(max_length=255, verbose_name='Jenis Biaya')),
                ('unit_price', models.CharField(max_length=255, verbose_name='Unit Price')),
            ],
            options={
                'verbose_name_plural': 'Master Beban',
            },
        ),
        migrations.CreateModel(
            name='Karyawan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=191, verbose_name='Nama Karyawan')),
                ('hp', models.CharField(max_length=21, verbose_name='Nomor HP')),
                ('email', models.CharField(max_length=191, verbose_name='Email')),
                ('jabatan', models.CharField(max_length=191, verbose_name='Jabatan')),
                ('alamat', models.TextField(verbose_name='Alamat')),
            ],
            options={
                'verbose_name_plural': 'Manajemen Karyawan',
            },
        ),
        migrations.CreateModel(
            name='KasKecil',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tgl_pencatatan', models.DateTimeField(blank=True, null=True)),
                ('no_kas', models.CharField(max_length=20)),
                ('nominal', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_created_kaskecil_by', to=settings.AUTH_USER_MODEL)),
                ('nama_karyawan', models.ForeignKey(blank=True, db_column='karyawan_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_karyawan', to='src.karyawan')),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_updated_kaskecil_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Kas Kecil',
            },
        ),
        migrations.CreateModel(
            name='Lembaga',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama_lembaga', models.CharField(max_length=191, verbose_name='Nama Lembaga/Instansi')),
                ('hp', models.CharField(max_length=21, verbose_name='Nomor HP')),
                ('email', models.CharField(max_length=191, verbose_name='Email')),
                ('alamat', models.TextField(verbose_name='Alamat')),
                ('pic', models.CharField(default='', max_length=255, verbose_name='Pic')),
            ],
            options={
                'verbose_name_plural': 'Manajemen Lembaga/Instansi',
            },
        ),
        migrations.CreateModel(
            name='MasterPersen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_persen', models.CharField(blank=True, max_length=100, null=True)),
                ('angka', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Manajemen Persentase',
            },
        ),
        migrations.CreateModel(
            name='MasterStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama_status', models.CharField(max_length=191)),
            ],
            options={
                'verbose_name_plural': 'Master Status',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=191, unique=True)),
                ('display_name', models.CharField(blank=True, max_length=191, null=True)),
                ('description', models.CharField(blank=True, max_length=191, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'MASTER ROLE',
            },
        ),
        migrations.CreateModel(
            name='TotalKasBesarKeluar',
            fields=[
                ('id', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('total_kas', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Total Kas Besar Keluar',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama_vendor', models.CharField(max_length=191, verbose_name='Nama Vendor')),
                ('hp', models.CharField(max_length=21, verbose_name='Nomor HP')),
                ('email', models.CharField(max_length=191, verbose_name='Email')),
                ('alamat', models.TextField(verbose_name='Alamat')),
                ('pic', models.CharField(default='', max_length=255, verbose_name='Pic')),
            ],
            options={
                'verbose_name_plural': 'Manajemen Vendor',
            },
        ),
        migrations.CreateModel(
            name='Stok',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_code', models.CharField(max_length=191, unique=True)),
                ('nama_barang', models.CharField(max_length=191, verbose_name='Nama Barang')),
                ('harga_jual', models.FloatField(blank=True, null=True, verbose_name='Harga Jual')),
                ('harga_beli', models.FloatField(blank=True, null=True, verbose_name='Harga Beli')),
                ('stok', models.IntegerField()),
                ('size', models.CharField(max_length=191)),
                ('tgl_terima_stok', models.DateTimeField(verbose_name='Tanggal Terima Stok')),
                ('id_vendor', models.ForeignKey(blank=True, db_column='vendor_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_vendor_id', to='src.vendor')),
            ],
            options={
                'verbose_name_plural': 'Manajemen Stok',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invoice_no', models.CharField(max_length=191, unique=True)),
                ('transaction_date', models.DateTimeField()),
                ('pic', models.CharField(blank=True, max_length=255, null=True)),
                ('total', models.FloatField()),
                ('tax', models.FloatField()),
                ('overdue', models.DateTimeField(blank=True, null=True)),
                ('discount', models.FloatField(blank=True, null=True)),
                ('total_amount', models.FloatField()),
                ('dp', models.FloatField(blank=True, null=True)),
                ('sisa_pembayaran', models.FloatField()),
                ('surat_pesanan_instansi', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_created_sale_by', to=settings.AUTH_USER_MODEL)),
                ('receiver_name', models.ForeignKey(blank=True, db_column='karyawan_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_karyawan_ss', to='src.karyawan')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_status', to='src.masterstatus')),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_updated_sale_by', to=settings.AUTH_USER_MODEL)),
                ('vendor_name', models.ForeignKey(blank=True, db_column='lembaga_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_lembaga', to='src.lembaga')),
            ],
            options={
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_code', models.CharField(blank=True, max_length=191, null=True)),
                ('quantity', models.SmallIntegerField()),
                ('size', models.CharField(blank=True, max_length=191, null=True)),
                ('unit_price', models.FloatField()),
                ('amount', models.FloatField()),
                ('product_name', models.ForeignKey(db_column='product_stok', on_delete=django.db.models.deletion.CASCADE, related_name='has_stok_sale', to='src.stok')),
                ('ss', models.ForeignKey(db_column='sale_id', on_delete=django.db.models.deletion.CASCADE, related_name='has_sale_detail', to='src.sales')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_status_detail', to='src.masterstatus')),
            ],
            options={
                'verbose_name_plural': 'Sale Detail',
            },
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invoice_no', models.CharField(max_length=191)),
                ('transaction_date', models.DateTimeField()),
                ('total', models.FloatField()),
                ('tax_persen', models.FloatField(blank=True, null=True)),
                ('tax', models.FloatField()),
                ('no_purchase_order', models.CharField(default='', max_length=100)),
                ('total_amount', models.FloatField()),
                ('ongkos_kirim', models.FloatField(blank=True, null=True)),
                ('nomor_surat_jalan', models.CharField(blank=True, max_length=100, null=True)),
                ('dp', models.FloatField(blank=True, default=0, null=True)),
                ('dp_persen', models.FloatField(blank=True, null=True)),
                ('sisa_pembayaran', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_created_by', to=settings.AUTH_USER_MODEL)),
                ('receiver_name', models.ForeignKey(blank=True, db_column='karyawan_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_karyawan_ps', to='src.karyawan')),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_updated_by', to=settings.AUTH_USER_MODEL)),
                ('vendor_name', models.ForeignKey(blank=True, db_column='vendor_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_vendor', to='src.vendor')),
            ],
            options={
                'verbose_name_plural': 'Purchases',
            },
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_code', models.CharField(blank=True, max_length=191, null=True)),
                ('quantity', models.SmallIntegerField()),
                ('size', models.CharField(blank=True, max_length=191, null=True)),
                ('unit_price', models.FloatField()),
                ('amount', models.FloatField()),
                ('product_name', models.ForeignKey(db_column='product_stok', on_delete=django.db.models.deletion.CASCADE, related_name='has_stok_ps', to='src.stok')),
                ('ps', models.ForeignKey(db_column='purchase_id', on_delete=django.db.models.deletion.CASCADE, related_name='has_purchase_detail', to='src.purchases')),
            ],
            options={
                'verbose_name_plural': 'Purchases Detail',
            },
        ),
        migrations.CreateModel(
            name='KasKecilDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('jenis_kebutuhan', models.CharField(max_length=191)),
                ('quantity', models.SmallIntegerField()),
                ('unit_price', models.FloatField()),
                ('amount', models.FloatField()),
                ('id_kebutuhan', models.ForeignKey(db_column='id_kebutuhan', on_delete=django.db.models.deletion.CASCADE, related_name='has_kebutuhan_detail', to='src.beban')),
                ('kk', models.ForeignKey(db_column='kaskecil_id', on_delete=django.db.models.deletion.CASCADE, related_name='has_kaskecil_detail', to='src.kaskecil')),
            ],
            options={
                'verbose_name_plural': 'Kas Kecil Detail',
            },
        ),
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
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_created_kasbesarmasuk_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_updated_kasbesarmasuk_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Kas Besar Masuk',
            },
        ),
        migrations.CreateModel(
            name='KasBesarKeluar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tgl_pencatatan', models.DateTimeField(blank=True, null=True)),
                ('nominal', models.FloatField()),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_created_kasbesarkeluar_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_updated_kasbesarkeluar_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Kas Besar Keluar',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(to='src.Roles'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
