from django import forms
from django.db.models import fields
from src.models import *

class KasBesarMasukForm(forms.ModelForm):

    class Meta:
        model = KasBesarMasuk
        fields = ('tgl_pencatatan','no_transaksi','pengirim','bank_pengirim','nominal')

    def __init__(self, *args, **kwargs):
        super(KasBesarMasukForm, self).__init__(*args, **kwargs)
        self.fields["tgl_pencatatan"].required = True
        self.fields["no_transaksi"].required = True
        self.fields["pengirim"].required = True
        self.fields["bank_pengirim"].required = True
        self.fields["nominal"].required = True
        self.fields['tgl_pencatatan'].widget.attrs['class'] = "form-control"
        self.fields['no_transaksi'].widget.attrs['class'] = "form-control"
        self.fields['pengirim'].widget.attrs['class'] = "form-control"
        self.fields['bank_pengirim'].widget.attrs['class'] = "form-control"
        self.fields['nominal'].widget.attrs['class'] = "form-control"
        
class KasBesarKeluarForm(forms.ModelForm):
    
    class Meta:
        model = KasBesarKeluar
        fields = ('tgl_pencatatan', 'keterangan', 'nominal')
                  
    def __init__(self, *args, **kwargs):
        super(KasBesarKeluarForm, self).__init__(*args, **kwargs)
        self.fields["tgl_pencatatan"].required = True
        self.fields["keterangan"].required = True
        self.fields["nominal"].required = True
        self.fields['tgl_pencatatan'].widget.attrs['class'] = "form-control"
        self.fields['keterangan'].widget.attrs['class'] = "form-control"
        self.fields['nominal'].widget.attrs['class'] = "form-control"

class KasKecilForm(forms.ModelForm):

    class Meta:
        model = KasKecil
        fields = ('tgl_pencatatan','no_kas','nama_karyawan')

    def __init__(self, *args, **kwargs):
        super(KasKecilForm, self).__init__(*args, **kwargs)
        self.fields["tgl_pencatatan"].required = True
        self.fields["no_kas"].required = True
        self.fields["nama_karyawan"].required = True
        self.fields['tgl_pencatatan'].widget.attrs['class'] = "form-control"
        self.fields['no_kas'].widget.attrs['class'] = "form-control"
        self.fields['nama_karyawan'].widget.attrs['class'] = "form-control"

class KasKecilFormEdit(forms.ModelForm):

    class Meta:
        model = KasKecil
        fields = ('tgl_pencatatan','nama_karyawan','no_kas')

    def __init__(self, *args, **kwargs):
        super(KasKecilFormEdit, self).__init__(*args, **kwargs)
        self.fields["tgl_pencatatan"].required = True
        self.fields["no_kas"].required = True
        self.fields["nama_karyawan"].required = True
        self.fields['tgl_pencatatan'].widget.attrs['class'] = "form-control"
        self.fields['no_kas'].widget.attrs['class'] = "form-control"
        self.fields['nama_karyawan'].widget.attrs['class'] = "form-control"

class KasKecilFormEdit2(forms.ModelForm):

    class Meta:
        model = KasKecil
        fields = ('nama_karyawan',)

    def __init__(self, *args, **kwargs):
        super(KasKecilFormEdit2, self).__init__(*args, **kwargs)
        self.fields["nama_karyawan"].required = True

class KasKecilDetailForm(forms.ModelForm):

    class Meta:
        model = KasKecilDetail
        fields = ("id_kebutuhan","jenis_kebutuhan","quantity","unit_price",)

    def __init__(self, *args, **kwargs):
        super(KasKecilDetailForm, self).__init__(*args, **kwargs)
        self.fields["id_kebutuhan"].required = True
        self.fields["jenis_kebutuhan"].required = True
        self.fields["quantity"].required = True
        self.fields["unit_price"].required = True
        self.fields['id_kebutuhan'].widget.attrs['class'] = "form-control"
        self.fields['jenis_kebutuhan'].widget.attrs['class'] = "form-control"
        self.fields['quantity'].widget.attrs['class'] = "form-control"
        self.fields['unit_price'].widget.attrs['class'] = "form-control"