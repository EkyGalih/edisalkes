from django.contrib import admin
from django.contrib.admin.helpers import Fieldset
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import Group
from src.forms import *
from src.models import *

# from import_export.admin import ImportExportActionModelAdmin

admin.site.register(Roles)
admin.site.register(MasterStatus)
admin.site.register(Karyawan)
admin.site.register(Vendor)
admin.site.register(Lembaga)
admin.site.register(MasterPersen)
admin.site.register(Beban)

@admin.register(Stok)
class StokAdmin(admin.ModelAdmin):
    # list_display = ('kode_pulau','nama_pulau','status')
    list_display = ("nama_barang","harga_jual", "harga_beli","stok","size","tgl_terima_stok")
    list_filter = ()
    list_per_page = 20
    search_fields = ('nama_barang','stok')
    ordering = ('harga_jual',)

    # fields = ["nama_barang","id_barang","harga_jual", "harga_beli","stok","size"]

# admin.site.register(Stok)
# @admin.register(Karyawan)
# class KaryawanAdmin(BaseUserAdmin):
#     fieldsets
# class StokAdmin(admin.ModelAdmin):
#     list_display = ('nama_barang', 'id_vendor','harga_jual','harga_beli','stok')
    
#     def get_author(self, obj):
#         return obj.book.author
#     get_author.short_description = 'Stok Admin'
#     get_author.admin_order_field = 'nama_barang'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'roles', 'group')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email','group')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    # raw_id_fields = ('group',)