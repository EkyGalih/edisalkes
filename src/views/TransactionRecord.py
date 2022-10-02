from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from src.forms import SalesForm, VendorForm, LembagaForm
from src.forms.lembaga_forms import PicForm
from src.forms.purchase_forms import PurchaseDetailForm, PurchaseForm, PurchaseFormEdit
from src.forms.sales_forms import SalesFormEdit, SalesDetailForm, SalesFormEdit2
from src.models import Sales, SaleDetail, Stok, Karyawan, Vendor, Lembaga, MasterPersen
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.template.loader import get_template, render_to_string
from datetime import date
import datetime

from src.models.TransactionRecord_M import MasterPersen, MasterStatus, PurchaseDetail, Purchases

@login_required
def purhases(request):
    frm = PurchaseForm
    frm_ven = VendorForm
    purchase_list = Purchases.objects.filter(created_by=request.user)
    status_ven = 0
    if "q" in request.GET and request.GET["q"] != "":
        purchase_list = Purchases.objects.filter(created_by=request.user, invoice_no=request.GET['q'])
    if request.POST:
        if "invoice_no" in request.POST:
            frm = PurchaseForm(request.POST)
            if frm.is_valid():
                addfrm = frm.save(commit=False)
                addfrm.created_by = request.user
                addfrm.total = 0
                addfrm.total_amount = 0
                addfrm.dp =0
                addfrm.save()
                messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
                return redirect(reverse('core:purchases_detail', kwargs={'pk':addfrm.pk}))
            else:
                print("form tidak valid")
        else:
            frm_ven = VendorForm(request.POST)
            if frm_ven.is_valid():
                frm_ven.save()
                messages.add_message(request, messages.INFO, mark_safe('vendor added.'))
                status_ven=1
            print(frm_ven.errors)

    context = {"frm":frm,"purcs":purchase_list,'frm_ven':frm_ven,'status_ven':status_ven}
    return render(request,'backend/purchases.html', context)

@login_required
def purchaseDetail(request,pk):
    tr_obj = Purchases.objects.get(pk=pk)
    purchase_item = PurchaseDetail.objects.filter(ps=pk)
    frm = PurchaseFormEdit(instance=tr_obj)
    frm2 = PurchaseDetailForm
    kar = Karyawan.objects.all()
    vend = Vendor.objects.all()
    if request.POST:
        # print(request.POST)
        # print(request.POST["receiver_name"])
        # print("berhasil masuk post")
        frm = PurchaseFormEdit(request.POST,instance=tr_obj)
        frm2 = PurchaseDetailForm(request.POST)
        if frm.is_valid():
            # print("oke berubah")
            frmadd = frm.save(commit=False)
            if frm2.is_valid():
                frm2add = frm2.save(commit=False)
                frm2add.ps = tr_obj
                frm2add.unit_price = request.POST['unit_price']
                frm2add.amount = float(frm2add.quantity) * float(frm2add.unit_price)
                frmadd.total += frm2add.amount
                frmadd.tax = (float(frmadd.tax_persen)/100) * float(frmadd.total)
                ongkos_kirim = 0
                if frmadd.ongkos_kirim:
                    ongkos_kirim = float(frmadd.ongkos_kirim)
                frmadd.total_amount = float(frmadd.total) + ongkos_kirim + frmadd.tax
                
                frm2add.save()
                frmadd.save()
                messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
                return redirect(reverse('core:purchases_detail', kwargs={'pk':pk}))
            
            nilai_total = float(frmadd.total) 
            nilai_persen = (float(frmadd.tax_persen)/100)
            frmadd.tax = (nilai_persen * nilai_total)
            ongkos_kirim = 0
            if frmadd.ongkos_kirim:
                ongkos_kirim = float(frmadd.ongkos_kirim)
            frmadd.total_amount = float(frmadd.total) + ongkos_kirim + frmadd.tax
            # frmadd.total_amount = float(frmadd.total) + frmadd.tax
            frmadd.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return redirect(reverse('core:purchases'))
        print(frm.errors)
        print(frm2.errors)
        messages.add_message(request, messages.INFO, mark_safe('Harap melengkapi form karyawan penerima'))
        return redirect(reverse('core:purchases_detail', kwargs={'pk':pk}))
        
    context = {"trs":tr_obj, "frm2":frm2,"purchase_item":purchase_item,"frm":frm,"kar":kar,"vend":vend}
    return render(request, "backend/detail-purchase.html",context)

@login_required
def edittemplateitemps(request,pk):
    tr_obj = PurchaseDetail.objects.get(pk=pk)
    frm = PurchaseDetailForm(request.POST, instance=tr_obj)
    stok = Stok.objects.all()
    mstat = MasterStatus.objects.all()
    # print(frm)
    html  = render_to_string("backend/particial-modal/form-edit-template-ps.html",{"frm":frm,"trs":tr_obj,"stts":mstat,'stok':stok})
    data = {'html': html}
    return JsonResponse(data)

@login_required
def edititempurchase(request,pk):
    print(pk)
    tr_obj = PurchaseDetail.objects.get(pk=pk)
    print(tr_obj.amount)
    amount_item_f = tr_obj.amount
    ps = tr_obj.ps.pk
    tr2_obj = Purchases.objects.get(pk=ps)
    if request.POST:
        frm2 = PurchaseDetailForm(request.POST, instance=tr_obj)
        
        if frm2.is_valid():
            frm2add = frm2.save(commit=False)
            frm2add.unit_price = request.POST['unit_price']
            frm2add.amount = float(frm2add.quantity) * float(frm2add.unit_price)
            tr2_obj.total = (tr2_obj.total - amount_item_f) + float(frm2add.amount)
            tr2_obj.tax = (float(tr2_obj.tax_persen)/100) * float(tr2_obj.total)
            ongkos_kirim = 0
            if tr2_obj.ongkos_kirim:
                ongkos_kirim = float(tr2_obj.ongkos_kirim)
            tr2_obj.total_amount = float(tr2_obj.total) + ongkos_kirim + tr2_obj.tax
            # tr2_obj.total_amount = float(tr2_obj.total) + tr2_obj.tax
            frm2add.save()
            tr2_obj.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return JsonResponse({'result':True})
        
        return JsonResponse({'result':False})
    return redirect(reverse('core:purchases_detail', kwargs={'pk':ps}))

@login_required
def deletePurchase(request,pk):
    purchase = Purchases.objects.get(pk=pk)
    if request.POST:
        try:
            purchase.delete()
            return JsonResponse({'result':True})
        except:
            return JsonResponse({'result':False})
    return JsonResponse({'result':False,'method':'get'})

@login_required
def deleteItemPurchase(request, pk):
    item_purchase = PurchaseDetail.objects.get(pk=pk)
    purchase = Purchases.objects.get(pk=item_purchase.ps.pk)
    amount_item_f = item_purchase.amount

    # tambahkan hapus total dengan kurangi total sebelum dihapus
    if request.POST:
        try:
            purchase.total -= amount_item_f
            purchase.tax = (float(purchase.tax_persen)/100) * purchase.total
            ongkos_kirim = 0
            if purchase.ongkos_kirim:
                ongkos_kirim = float(purchase.ongkos_kirim)
            purchase.total_amount = float(purchase.total) + ongkos_kirim + float(purchase.tax)
            # purchase.total_amount = (float(purchase.total) + float(purchase.tax))
            purchase.save()
            item_purchase.delete()
            return JsonResponse({'result':True})
        except:
            return JsonResponse({'result':False})
    return JsonResponse({'result':False,'methode':'GET'})

    # =================================

@login_required
def sales(request):
    frm = SalesForm
    frm_pel = LembagaForm
    sale_list = Sales.objects.filter(created_by=request.user)
    status_pel = 0
    pic = PicForm
    if "q" in request.GET and request.GET["q"] != "":
        sale_list = Sales.objects.filter(created_by=request.user, invoice_no=request.GET['q'])
    if request.POST:
        print("berhasil masuk post")
        if "transaction_date" in request.POST:
            frm = SalesForm(request.POST)
            if frm.is_valid():
                # try:
                addfrm = frm.save(commit=False)
                addfrm.created_by = request.user
                addfrm.total = 0
                addfrm.total_amount = 0
                # addfrm.tax = 0
                addfrm.dp =0
                # addfrm.sisa_pembayaran = 0
                addfrm.save()
                print("lolos")
                messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
                return redirect(reverse('core:sales_detail', kwargs={'pk':addfrm.pk}))
                # except:
                #     print(frm)
                #     messages.add_message(request, messages.WARNING, mark_safe('Gagal disimpan.'))
                #     return redirect(reverse('core:sales'))
            else:
                print("form tidak valid")
        else:
            frm_pel = LembagaForm(request.POST)
            if frm_pel.is_valid():
                frm_pel.save()
                messages.add_message(request, messages.INFO, mark_safe('pelanggan added.'))
                status_pel=1
    context = {"frm":frm,"sls":sale_list,"frm_pel":frm_pel,"status_pel":status_pel,"pic":pic}
    return render(request,'backend/sales.html',context)

@login_required
def salesDetail(request,pk):
    tr_obj = Sales.objects.get(pk=pk)
    persen_pajak = MasterPersen.objects.get(pk=1).angka
    
    due_date = tr_obj.overdue
    sale_item = SaleDetail.objects.filter(ss=pk)
    frm = SalesFormEdit(instance=tr_obj)
    frm2 = SalesDetailForm
    kar = Karyawan.objects.all()
    pel = Lembaga.objects.all()
    if request.POST:
        # print(request.POST["receiver_name"])
        print("berhasil masuk post")
        frm = SalesFormEdit(request.POST,instance=tr_obj)
        frm2 = SalesDetailForm(request.POST)
        if frm.is_valid():
            frmadd = frm.save(commit=False)
            
            if frm2.is_valid():
                frm2add = frm2.save(commit=False)
                frm2add.ss = tr_obj
                frm2add.amount = float(frm2add.quantity) * float(frm2add.unit_price)
                frmadd.total += frm2add.amount
                frmadd.tax = 0.125 * float(frmadd.total)
                diskon = float(frmadd.discount)/100 * frmadd.total 
                frmadd.total_amount = float(frmadd.total) - diskon + frmadd.tax
                frm2add.save()
                frmadd.save()
                messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
                return redirect(reverse('core:sales_detail', kwargs={'pk':pk}))
            # frmadd.total += frm2add.amount
            frmadd.tax = 0.125 * float(frmadd.total)
            diskon = float(frmadd.discount)/100 * frmadd.total 
            frmadd.total_amount = float(frmadd.total) - diskon + frmadd.tax
            # print(frmadd.discount)
            # frmadd.total_amount = float(frmadd.total) + frmadd.tax
            frmadd.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return redirect(reverse('core:sales'))
        
        messages.add_message(request, messages.INFO, mark_safe('Harap melengkapi form Nama Petugas'))
        return redirect(reverse('core:sales_detail', kwargs={'pk':pk}))
        
    context = {"trs":tr_obj, "frm2":frm2,"sale_item":sale_item,"frm":frm,"kar":kar,"pel":pel,"due_date":due_date,'persen_pajak':persen_pajak}
    return render(request, "backend/detail-sales.html",context)

@login_required
def edittemplateitem(request,pk):
    tr_obj = SaleDetail.objects.get(pk=pk)
    frm = SalesDetailForm(request.POST, instance=tr_obj)
    mstat = MasterStatus.objects.all()
    stok = Stok.objects.all()
    # print(frm)
    html  = render_to_string("backend/particial-modal/form-edit-item.html",{"frm":frm,"trs":tr_obj,"stts":mstat,'stok':stok})
    data = {'html': html}
    return JsonResponse(data)

@login_required
def edititemsale(request,pk):
    print(pk)
    tr_obj = SaleDetail.objects.get(pk=pk)
    print(tr_obj.amount)
    amount_item_f = tr_obj.amount
    ss = tr_obj.ss.pk
    tr2_obj = Sales.objects.get(pk=ss)
    if request.POST:
        frm2 = SalesDetailForm(request.POST, instance=tr_obj)
        
        if frm2.is_valid():
            frm2add = frm2.save(commit=False)
            # frm2add.ss = ss
            frm2add.amount = float(frm2add.quantity) * float(frm2add.unit_price)
            # print("amount post detail :"+ str(frm2add.amount))
            # print("amount total keseluruhan awal: "+str(tr2_obj.total))
            # print("amount detail before:"+str(amount_item_f))
            # print('amount total keseluruhan awal - amount detail before + amount post detail = ')
            # print((tr2_obj.total - amount_item_f) + float(frm2add.amount))
            # print(frm2add.amount)
            tr2_obj.total = (tr2_obj.total - amount_item_f) + float(frm2add.amount)
            tr2_obj.tax = 0.125 * float(tr2_obj.total)
            diskon = float(tr2_obj.discount)/100 * tr2_obj.total 
            tr2_obj.total_amount = float(tr2_obj.total) - diskon + tr2_obj.tax
            # tr2_obj.total_amount = float(tr2_obj.total) + tr2_obj.tax
            frm2add.save()
            tr2_obj.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return JsonResponse({'result':True})
        
        return JsonResponse({'result':False})
    return redirect(reverse('core:sales_detail', kwargs={'pk':ss}))

@login_required
def deleteSale(request,pk):
    sale = Sales.objects.get(pk=pk)
    if request.POST:
        try:
            sale.delete()
            return JsonResponse({'result':True})
        except:
            return JsonResponse({'result':False})
    return JsonResponse({'result':False,'method':'get'})

@login_required
def deleteItemSale(request, pk):
    item_sale = SaleDetail.objects.get(pk=pk)
    sale = Sales.objects.get(pk=item_sale.ss.pk)
    amount_item_f = item_sale.amount
    

    # tambahkan hapus total dengan kurangi total sebelum dihapus DONE
    if request.POST:
        try:
            sale.total -= amount_item_f
            sale.tax = 0.1 * sale.total
            diskon = float(sale.discount)/100 * sale.total 
            sale.total_amount = float(sale.total) - diskon + sale.tax
            # sale.total_amount = (float(sale.total) + float(sale.tax))
            sale.save()
            item_sale.delete()
            return JsonResponse({'result':True})
        except:
            return JsonResponse({'result':False})
    return JsonResponse({'result':False,'methode':'GET'})
