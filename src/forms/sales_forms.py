from django import forms
from django.db.models import fields
from src.models import *
from django.forms.widgets import Select, SelectMultiple
from django.forms import ModelChoiceField

class SalesForm(forms.ModelForm):

    class Meta:
        model = Sales
        fields = ('transaction_date','vendor_name', 'pic')

    def __init__(self, *args, **kwargs):
        super(SalesForm, self).__init__(*args, **kwargs)
        self.fields["transaction_date"].required = True
        self.fields["vendor_name"].required = True
        self.fields["pic"].required = True
        self.fields['transaction_date'].widget.attrs['class'] = "form-control"
        self.fields['vendor_name'].widget.attrs['class'] = "form-control"
        self.fields['pic'].widget.attrs['class'] = "form-control"
        

class SalesFormEdit(forms.ModelForm):

    class Meta:
        model = Sales
        fields = ('transaction_date','vendor_name','dp','receiver_name','discount')

    def __init__(self, *args, **kwargs):
        super(SalesFormEdit, self).__init__(*args, **kwargs)
        self.fields["transaction_date"].required = True
        self.fields["vendor_name"].required = True
        self.fields["receiver_name"].required = True
        self.fields['transaction_date'].widget.attrs['class'] = "form-control"
        self.fields['vendor_name'].widget.attrs['class'] = "form-control"
        self.fields['dp'].widget.attrs['class'] = "form-control"
        self.fields['receiver_name'].widget.attrs['class'] = "form-control"

class SalesFormEdit2(forms.ModelForm):

    class Meta:
        model = Sales
        fields = ('vendor_name',)

    def __init__(self, *args, **kwargs):
        super(SalesFormEdit2, self).__init__(*args, **kwargs)
        self.fields["vendor_name"].required = True

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
        for key,val in opt_attrs.items():
            option_dict['attrs'][key] = val
        return option_dict

class HargaChoiceField(ModelChoiceField):
# Use our custom widget:
    widget = SelectWithOptionAttribute

    def label_from_instance(self, obj):
    # 'obj' will be an Ingredient
        return {
            # the usual label:
            'label': super().label_from_instance(obj),
            # the new data attribute:
            'data-price': obj.harga_jual
        }

class SalesDetailForm(forms.ModelForm):

    class Meta:
        model = SaleDetail
        fields = ("product_code","product_name","quantity","size","unit_price","status",)

        field_classes = {
            'product_name': HargaChoiceField
        }
        
    def __init__(self, *args, **kwargs):
        super(SalesDetailForm, self).__init__(*args, **kwargs)
        # self.fields["product_code"].required = True
        self.fields["product_name"].required = True
        self.fields["quantity"].required = True
        # self.fields["size"].required = True
        self.fields["unit_price"].required = True
        self.fields["status"].required = True
        self.fields['product_code'].widget.attrs['hidden'] = "hidden"
        self.fields['product_name'].widget.attrs['class'] = "form-control"
        self.fields['quantity'].widget.attrs['class'] = "form-control"
        self.fields['size'].widget.attrs['hidden'] = "hidden"
        self.fields['unit_price'].widget.attrs['class'] = "form-control"
        self.fields['status'].widget.attrs['class'] = "form-control"
