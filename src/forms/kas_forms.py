from django import forms
from django.db.models import fields
from src.models import *
from django.forms.widgets import Select, SelectMultiple
from django.forms import ModelChoiceField

class KasBesarMasukForm(forms.ModelForm):

    class Meta:
        model = KasBesarMasuk
        fields = ('tgl_pencatatan', 'no_transaksi',
                  'pengirim', 'bank_pengirim', 'nominal')

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


class TotalKasBesarKeluarForm(forms.ModelForm):

    class Meta:
        model = TotalKasBesarKeluar
        fields = ('total_kas',)

    def __init__(self, *args, **kwargs):
        super(TotalKasBesarKeluarForm, self).__init__(*args, **kwargs)
        self.fields["total_kas"].required = True
        self.fields['total_kas'].widget.attrs['class'] = "form-control"


class KasKecilMasukForm(forms.ModelForm):

    class Meta:
        model = KasBesarKeluar
        fields = ('tgl_pencatatan', 'keterangan', 'nominal')

    def __init__(self, *args, **kwargs):
        super(KasKecilMasukForm, self).__init__(*args, **kwargs)
        self.fields["tgl_pencatatan"].required = True
        self.fields["keterangan"].required = True
        self.fields["nominal"].required = True
        self.fields['tgl_pencatatan'].widget.attrs['class'] = "form-control"
        self.fields['keterangan'].widget.attrs['class'] = "form-control"
        self.fields['nominal'].widget.attrs['class'] = "form-control"


class KasKecilKeluarForm(forms.ModelForm):

    class Meta:
        model = KasKecil
        fields = ('tgl_pencatatan', 'no_kas', 'nama_karyawan')

    def __init__(self, *args, **kwargs):
        super(KasKecilKeluarForm, self).__init__(*args, **kwargs)
        self.fields["tgl_pencatatan"].required = True
        self.fields["no_kas"].required = True
        self.fields["nama_karyawan"].required = True
        self.fields['tgl_pencatatan'].widget.attrs['class'] = "form-control"
        self.fields['no_kas'].widget.attrs['class'] = "form-control"
        self.fields['nama_karyawan'].widget.attrs['class'] = "form-control"


class KasKecilFormEdit(forms.ModelForm):

    class Meta:
        model = KasKecil
        fields = ('tgl_pencatatan', 'nama_karyawan', 'no_kas')

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

class SelectWithOptionAttribute(Select):

    def create_option(self, name, value, label, selected, index,
                      subindex=None, attrs=None):
        # This allows using strings labels as usual
        if isinstance(label, dict):
            opt_attrs = label.copy()
            label = opt_attrs.pop('label')
        else:
            opt_attrs = {}
        option_dict = super().create_option(name, value,
                                            label, selected, index, subindex=subindex, attrs=attrs)
        for key, val in opt_attrs.items():
            option_dict['attrs'][key] = val
        return option_dict


class BebanChoiceField(ModelChoiceField):
    # Use our custom widget:
    widget = SelectWithOptionAttribute

    def label_from_instance(self, obj):
        # 'obj' will be an Ingredient
        return {
            # the usual label:
            'label': super().label_from_instance(obj),
            # the new data attribute:
            'data-price': obj.unit_price,
            'data-beban': obj.jenis_biaya
        }


class KasKecilDetailForm(forms.ModelForm):

    class Meta:
        model = KasKecilDetail
        fields = ("id_kebutuhan", "jenis_kebutuhan", "quantity", "unit_price",)

        field_classes = {
            'id_kebutuhan' : BebanChoiceField
        }

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
