from email.policy import default
from enum import unique
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from src.models import User
import uuid
from datetime import date, timedelta
import datetime


class MasterPersen(models.Model):
    nama_persen = models.CharField(max_length=100, blank=True, null=True)
    angka = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.nama_persen

    class Meta:
        verbose_name_plural = 'Manajemen Persentase'


# def get_tax_persen():
tax_value = MasterPersen.objects.get(pk=1)
HASIL_PERSEN_TAX = 0
if tax_value:
    HASIL_PERSEN_TAX = float(tax_value.angka)/100


class Lembaga(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_lembaga = models.CharField('Nama Lembaga/Instansi', max_length=191)
    hp = models.CharField('Nomor HP', max_length=21)
    email = models.CharField('Email', max_length=191)
    alamat = models.TextField('Alamat')
    pic = models.CharField('Pic', max_length=255, default="")

    def __str__(self):
        return self.nama_lembaga

    class Meta:
        verbose_name_plural = 'Manajemen Lembaga/Instansi'


class Karyawan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField('Nama Karyawan', max_length=191)
    hp = models.CharField('Nomor HP', max_length=21)
    email = models.CharField('Email', max_length=191)
    jabatan = models.CharField('Jabatan', max_length=191)
    alamat = models.TextField('Alamat')

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = 'Manajemen Karyawan'


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_vendor = models.CharField('Nama Vendor', max_length=191)
    hp = models.CharField('Nomor HP', max_length=21)
    email = models.CharField('Email', max_length=191)
    alamat = models.TextField('Alamat')
    pic = models.CharField('Pic', max_length=255, default="")

    def __str__(self):
        return self.nama_vendor

    class Meta:
        verbose_name_plural = 'Manajemen Vendor'


class Stok(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_code = models.CharField(unique=True, max_length=191)
    nama_barang = models.CharField('Nama Barang', max_length=191)
    id_vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL,
                                  db_column="vendor_id", related_name="has_vendor_id", blank=True, null=True)
    harga_jual = models.FloatField('Harga Jual', blank=True, null=True)
    harga_beli = models.FloatField('Harga Beli', blank=True, null=True)
    stok = models.IntegerField()
    size = models.CharField(max_length=191)
    tgl_terima_stok = models.DateTimeField('Tanggal Terima Stok')

    def __str__(self):
        return self.product_code + '-' + self.nama_barang + '-'+self.size

    class Meta:
        verbose_name_plural = 'Manajemen Stok'

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            today = date.today()
            today_string = today.strftime('%y%m%d')
            next_product_code = '01'
            last_product = Stok.objects.filter(
                product_code__startswith=today_string).order_by('product_code').last()
            if last_product:
                last_product_code = int(last_product.product_code[6:])
                next_product_code = '{0:02d}'.format(last_product_code + 1)
            self.product_code = today_string + next_product_code
        # print(self.invoice_no)
        super(Stok, self).save(*args, **kwargs)


class Purchases(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.CharField(max_length=191)
    transaction_date = models.DateTimeField()
    vendor_name = models.ForeignKey(Vendor, on_delete=models.SET_NULL,
                                    blank=True, null=True, db_column="vendor_id", related_name="has_vendor")
    total = models.FloatField()
    tax_persen = models.FloatField(blank=True, null=True)
    tax = models.FloatField()
    no_purchase_order = models.CharField(max_length=100, default="")
    total_amount = models.FloatField()
    ongkos_kirim = models.FloatField(blank=True, null=True)  # field tambahan
    nomor_surat_jalan = models.CharField(
        max_length=100, blank=True, null=True)  # field tambahan
    dp = models.FloatField(default=0, null=True, blank=True)
    dp_persen = models.FloatField(blank=True, null=True)
    sisa_pembayaran = models.FloatField()
    receiver_name = models.ForeignKey(Karyawan, on_delete=models.SET_NULL, blank=True,
                                      null=True, db_column="karyawan_id", related_name="has_karyawan_ps")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='created_by',
                                   related_name='has_created_by', blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='updated_by',
                                   related_name='has_updated_by', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # self.tax = (0.1 * self.total)
        # self.sisa_pembayaran = (self.total_amount - self.dp)
        if (self.tax_persen == None):
            self.tax_persen = 0
        if (self.dp_persen == None):
            self.dp_persen = 0
        self.tax = (float(self.tax_persen)/100 * float(self.total))
        self.dp = (float(self.dp_persen)/100 * float(self.total_amount))
        self.sisa_pembayaran = (float(self.total_amount) - float(self.dp))
        super(Purchases, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Purchases'


class PurchaseDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ps = models.ForeignKey(Purchases, on_delete=models.CASCADE,
                           db_column="purchase_id", related_name="has_purchase_detail")
    product_code = models.CharField(max_length=191, blank=True, null=True)
    product_name = models.ForeignKey(
        Stok, on_delete=models.CASCADE, db_column="product_stok", related_name="has_stok_ps")
    quantity = models.SmallIntegerField()
    size = models.CharField(max_length=191, blank=True, null=True)
    unit_price = models.FloatField()
    amount = models.FloatField()

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = 'Purchases Detail'


class MasterStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_status = models.CharField(max_length=191)

    def __str__(self):
        return self.nama_status

    class Meta:
        verbose_name_plural = 'Master Status'


class Beban(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kode_beban = models.CharField("Id Beban/Biaya", unique=True, max_length=255, default="")
    jenis_biaya = models.CharField('Jenis Biaya', max_length=255)
    unit_price = models.CharField('Unit Price', max_length=255)

    def __str__(self):
        return self.jenis_biaya

    class Meta:
        verbose_name_plural = 'Master Beban'


class Sales(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.CharField(unique=True, max_length=191)
    transaction_date = models.DateTimeField()
    vendor_name = models.ForeignKey(Lembaga, on_delete=models.SET_NULL, blank=True,
                                    null=True, db_column="lembaga_id", related_name="has_lembaga")
    pic = models.CharField(max_length=255, blank=True, null=True)
    # pelanggan = models.ForeignKey(Pelanggan, on_delete=models.SET_NULL, blank=True, null=True, db_column="pelanggan_id", related_name="has_pelanggan")
    total = models.FloatField()
    tax = models.FloatField()
    overdue = models.DateTimeField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    total_amount = models.FloatField()
    dp = models.FloatField(blank=True, null=True)
    sisa_pembayaran = models.FloatField()
    receiver_name = models.ForeignKey(Karyawan, on_delete=models.SET_NULL, blank=True,
                                      null=True, db_column="karyawan_id", related_name="has_karyawan_ss")
    status = models.ForeignKey(MasterStatus, on_delete=models.SET_NULL,
                               related_name="has_status", blank=True, null=True)
    surat_pesanan_instansi = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='created_by',
                                   related_name='has_created_sale_by', blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='updated_by',
                                   related_name='has_updated_sale_by', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            today = date.today()
            today_string = today.strftime('%y%m%d')
            next_invoice_number = '001'
            last_invoice = Sales.objects.filter(
                invoice_no__startswith=today_string).order_by('invoice_no').last()
            if last_invoice:
                last_invoice_number = int(last_invoice.invoice_no[7:])
                next_invoice_number = '{0:03d}'.format(last_invoice_number + 1)
            self.invoice_no = today_string + next_invoice_number
        self.tax = HASIL_PERSEN_TAX * float(self.total)
        self.overdue = self.transaction_date + datetime.timedelta(30)
        self.sisa_pembayaran = (float(self.total_amount))
        # print(self.invoice_no)
        super(Sales, self).save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no

    class Meta:
        verbose_name_plural = 'Sales'


class SaleDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ss = models.ForeignKey(Sales, on_delete=models.CASCADE,
                           db_column="sale_id", related_name="has_sale_detail")
    product_code = models.CharField(max_length=191, blank=True, null=True)
    product_name = models.ForeignKey(
        Stok, on_delete=models.CASCADE, db_column="product_stok", related_name="has_stok_sale")
    quantity = models.SmallIntegerField()
    size = models.CharField(max_length=191, blank=True, null=True)
    unit_price = models.FloatField()
    amount = models.FloatField()
    status = models.ForeignKey(MasterStatus, on_delete=models.SET_NULL,
                               related_name="has_status_detail", blank=True, null=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = 'Sale Detail'


class KasKecil(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tgl_pencatatan = models.DateTimeField(blank=True, null=True)
    no_kas = models.CharField(max_length=20)
    nama_karyawan = models.ForeignKey(Karyawan, on_delete=models.SET_NULL,
                                      blank=True, null=True, db_column="karyawan_id", related_name="has_karyawan")
    nominal = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='created_by',
                                   related_name='has_created_kaskecil_by', blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='updated_by',
                                   related_name='has_updated_kaskecil_by', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.no_kas

    class Meta:
        verbose_name_plural = 'Kas Kecil'


class KasKecilDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kk = models.ForeignKey(KasKecil, on_delete=models.CASCADE,
                           db_column="kaskecil_id", related_name="has_kaskecil_detail")
    id_kebutuhan = models.ForeignKey(
        Beban, on_delete=models.CASCADE, db_column="id_kebutuhan", related_name="has_kebutuhan_detail")
    jenis_kebutuhan = models.CharField(max_length=191)
    quantity = models.SmallIntegerField()
    unit_price = models.FloatField()
    amount = models.FloatField()

    def __str__(self):
        return self.id_kebutuhan

    class Meta:
        verbose_name_plural = 'Kas Kecil Detail'


class KasBesarMasuk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tgl_pencatatan = models.DateTimeField(blank=True, null=True)
    no_transaksi = models.CharField(max_length=20)
    pengirim = models.CharField(max_length=191)
    bank_pengirim = models.CharField(max_length=191)
    nominal = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='created_by',
                                   related_name='has_created_kasbesarmasuk_by', blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='updated_by',
                                   related_name='has_updated_kasbesarmasuk_by', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.no_transaksi

    class Meta:
        verbose_name_plural = 'Kas Besar Masuk'


class KasBesarKeluar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tgl_pencatatan = models.DateTimeField(blank=True, null=True)
    nominal = models.FloatField()
    keterangan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='created_by',
                                   related_name='has_created_kasbesarkeluar_by', blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='updated_by',
                                   related_name='has_updated_kasbesarkeluar_by', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.tgl_pencatatan

    class Meta:
        verbose_name_plural = 'Kas Besar Keluar'


class TotalKasBesarKeluar(models.Model):
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    total_kas = models.FloatField()

    def __str__(self):
        return self.total_kas

    class Meta:
        verbose_name_plural = 'Total Kas Besar Keluar'
