from django.urls import path
from .views import Auth,Dashboard,TransactionRecord as TR
from .views import Kas as KS
from .views import Landing as LN

app_name = 'core'
urlpatterns = [
    # path('user/', Login.as_view(), name='users'),
    path('',LN.landing, name='landing'),
    path('dashboard/',Dashboard.dashboard, name='dashboard'),
    path('staff/login/', Auth.signin, name='login'),
    path('staf/logout/',Auth.signout, name="logout"),
    path('pembelian/',TR.purhases, name="purchases"),
    path('pembelian/detail/<str:pk>',TR.purchaseDetail, name="purchases_detail"),
    path('pembelian/detail/item/<str:pk>',TR.edititempurchase, name="purchase_item_edit"),
    path('pembelian/detail/item/template/<str:pk>',TR.edittemplateitemps, name="purchase_item_edit_template"),
    path('pembelian/delete/<str:pk>',TR.deletePurchase, name="delete_purchase"),
    path('pembelian/detail/delete/<str:pk>',TR.deleteItemPurchase, name="ps_delete_item"),
    path('penjualan/',TR.sales, name="sales"),
    path('penjualan/detail/<str:pk>',TR.salesDetail, name="sales_detail"),
    path('penjualan/detail/item/<str:pk>',TR.edititemsale, name="sale_item_edit"),
    path('penjualan/detail/item/template/<str:pk>',TR.edittemplateitem, name="sale_item_edit_template"),
    path('penjualan/delete/<str:pk>',TR.deleteSale, name="delete_sale"),
    path('penjualan/detail/delete/<str:pk>',TR.deleteItemSale, name="delete_item"),

    path('kas/kecil/masuk',KS.kaskecilMasuk, name="kaskecil-masuk"),
    path('kas/kecil/keluar',KS.kaskecilKeluar, name="kaskecil-keluar"),
    path('kas/kecil/detail/keluar/<str:pk>',KS.kaskecilDetailKeluar, name="kaskecil_detail_keluar"),
    path('kas/kecil/detail/item/<str:pk>',KS.edititemkaskecil, name="kaskecil_item_edit"),
    path('kas/kecil/detail/item/template/<str:pk>',KS.edittemplateitemkk, name="kaskecil_item_edit_template"),
    path('kas/kecil/delete/<str:pk>',KS.deleteKasKecil, name="delete_kaskecil"),
    path('kas/kecil/detail/delete/<str:pk>',KS.deleteItemKasKecil, name="kk_delete_item"),
    path('kas/kecil/masuk/<str:pk>',KS.editkaskecilMasuk, name="kaskecilmasuk_edit"),
    path('kas/kecil/masuk/template/<str:pk>',KS.edittemplatekkMasuk, name="kaskecilmasuk_edit_template"),
    path('kas/kecil/keluar/template/<str:pk>',KS.edittemplatekkKeluar, name="kaskecilKeluar_edit_template"),

    path('kas/besarkeluar',KS.kasbesarKeluar, name="kasbesar-keluar"),
    path('kas/besarmasuk',KS.kasbesarMasuk, name="kasbesar-masuk"),
    path('kas/besar/keluar/delete/<str:pk>',KS.deleteKasBesarKeluar, name="delete_kasbesar_keluar"),
    path('kas/besar/masuk/delete/<str:pk>',KS.deleteKasBesarMasuk, name="delete_kasbesar_masuk"),
    path('kas/besar/keluar/<str:pk>',KS.editkasbesarKeluar, name="kasbesarKeluar_edit"),
    path('kas/besar/masuk/<str:pk>',KS.editkasbesarMasuk, name="kasbesarMasuk_edit"),
    path('kas/besar/keluar/template/<str:pk>',KS.edittemplatekbKeluar, name="kasbesarKeluar_edit_template"),
    path('kas/besar/masuk/template/<str:pk>',KS.edittemplatekbMasuk, name="kasbesarMasuk_edit_template"),
]