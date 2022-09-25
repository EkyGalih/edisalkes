from django import forms
from django.db.models import fields
from src.models import *

class LembagaForm(forms.ModelForm):

    class Meta:
        model = Lembaga
        fields = ('nama_lembaga','hp','email','alamat')

    def __init__(self, *args, **kwargs):
        super(LembagaForm, self).__init__(*args, **kwargs)
        self.fields["nama_lembaga"].required = True
        # self.fields["transaction_date"].required = True
        # self.fields["vendor_name"].required = True
        self.fields['nama_pelanggan'].widget.attrs['class'] = "form-control"
        self.fields['hp'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['class'] = "form-control"
        self.fields['alamat'].widget.attrs['class'] = "form-control"