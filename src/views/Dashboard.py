from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from src.models.TransactionRecord_M import Purchases, Sales, Stok, Karyawan
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    jumlah_beli = Purchases.objects.filter(created_at__gte=datetime.now()-timedelta(days=7)).count()
    jumlah_beli2 = Purchases.objects.values('total_amount','created_at').annotate(total=Count('total_amount', filter=Q(created_at__gte=datetime.now()-timedelta(days=7))),beli=Sum('total_amount', filter=Q(created_at__gte=datetime.now()-timedelta(days=7))))
    jumlah_jual = Sales.objects.values('total_amount','created_at').annotate(jual=Sum('total_amount', filter=Q(created_at__gte=datetime.now()-timedelta(days=7))))
    ten_sale =  Sales.objects.values('total_amount','vendor_name__nama_lembaga','created_at').annotate(jual=Sum('total_amount', filter=Q(created_at__gte=datetime.now()-timedelta(days=7))))[:10]
    transaksi_beli = Purchases.objects.count()
    ten_ps =  Purchases.objects.values('total_amount','vendor_name__nama_vendor','created_at').annotate(jual=Sum('total_amount', filter=Q(created_at__gte=datetime.now()-timedelta(days=7))))[:10]
    sisa_stok = Stok.objects.values('stok').annotate(jumlah=Sum('stok'))
    kar = Karyawan.objects.annotate(penerima_beli=Count('has_karyawan_ps'), petugas_jual=Count('has_karyawan_ss')).order_by('-penerima_beli')[:10]
    # kar = Karyawan.objects..annotate(penerima_beli=Count('has_karyawan_ps'), petugas_jual=Count('has_karyawan_ss'))
    # print(kar)
    context = {'beli':jumlah_beli2,'jual':jumlah_jual, 'stok':sisa_stok, 'ten_sale':ten_sale,'ten_ps':ten_ps,'kar':kar,'transaksi_beli':transaksi_beli}
    return render(request,'backend/dashboard.html', context)