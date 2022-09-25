from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from src.forms.kas_forms import KasBesarForm, KasKecilDetailForm, KasKecilForm, KasKecilFormEdit
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.template.loader import get_template, render_to_string
from src.models.TransactionRecord_M import KasBesar, KasKecil, KasKecilDetail, Karyawan

@login_required
def kaskecil(request):
    frm = KasKecilForm
    kk_list = KasKecil.objects.filter(created_by=request.user)
    if "q" in request.GET and request.GET["q"] is not "":
        kk_list = KasKecil.objects.filter(created_by=request.user, no_kas=request.GET['q'])
    if request.POST:
        frm = KasKecilForm(request.POST)
        if frm.is_valid():
            addfrm = frm.save(commit=False)
            addfrm.created_by = request.user
            addfrm.nominal = 0
            addfrm.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return redirect(reverse('core:kaskecil_detail', kwargs={'pk':addfrm.pk}))
        else:
            print("form tidak valid")

    context = {"frm":frm,"kaskecil":kk_list}
    return render(request,'backend/kaskecil.html', context)

@login_required
def kaskecilDetail(request,pk):
    tr_obj = KasKecil.objects.get(pk=pk)
    kaskecil_item = KasKecilDetail.objects.filter(kk=pk)
    frm = KasKecilFormEdit(instance=tr_obj)
    frm2 = KasKecilDetailForm
    kar = Karyawan.objects.all()
    if request.POST:
        # print(request.POST["receiver_name"])
        print("berhasil masuk post")
        frm = KasKecilFormEdit(request.POST,instance=tr_obj)
        frm2 = KasKecilDetailForm(request.POST)
        if frm.is_valid():
            frmadd = frm.save(commit=False)
            
            if frm2.is_valid():
                frm2add = frm2.save(commit=False)
                frm2add.kk = tr_obj
                frm2add.amount = float(frm2add.quantity) * float(frm2add.unit_price)
                frmadd.nominal += frm2add.amount
                frm2add.save()
                frmadd.save()
                messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
                return redirect(reverse('core:kaskecil_detail', kwargs={'pk':pk}))
            frmadd.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return redirect(reverse('core:kaskecil_detail', kwargs={'pk':pk}))
        
    context = {"trs":tr_obj, "frm2":frm2,"kaskecil_item":kaskecil_item,"frm":frm,"kar":kar}
    return render(request, "backend/detail-kaskecil.html",context)

@login_required
def edittemplateitemkk(request,pk):
    tr_obj = KasKecilDetail.objects.get(pk=pk)
    frm = KasKecilDetailForm(request.POST, instance=tr_obj)
    # print(frm)
    html  = render_to_string("backend/particial-modal/form-edit-item-kk.html",{"frm":frm,"trs":tr_obj})
    data = {'html': html}
    return JsonResponse(data)

@login_required
def edititemkaskecil(request,pk):
    tr_obj = KasKecilDetail.objects.get(pk=pk)
    amount_item_f = tr_obj.amount
    kk = tr_obj.kk.pk
    tr2_obj = KasKecil.objects.get(pk=kk)
    if request.POST:
        frm2 = KasKecilDetailForm(request.POST, instance=tr_obj)
        
        if frm2.is_valid():
            frm2add = frm2.save(commit=False)
            frm2add.amount = float(frm2add.quantity) * float(frm2add.unit_price)
            tr2_obj.nominal = (tr2_obj.nominal - amount_item_f) + float(frm2add.amount)
            frm2add.save()
            tr2_obj.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return JsonResponse({'result':True})
        print(frm2.errors)
        print(frm2)
        return JsonResponse({'result':False})
    return redirect(reverse('core:kaskecil_detail', kwargs={'pk':kk}))

@login_required
def deleteKasKecil(request,pk):
    kk = KasKecil.objects.get(pk=pk)
    if request.POST:
        try:
            kk.delete()
            return JsonResponse({'result':True})
        except:
            return JsonResponse({'result':False})
    return JsonResponse({'result':False,'method':'get'})

@login_required
def deleteItemKasKecil(request, pk):
    item_kk = KasKecilDetail.objects.get(pk=pk)
    kk = KasKecil.objects.get(pk=item_kk.kk.pk)
    amount_item_f = item_kk.amount

    # tambahkan hapus total dengan kurangi total sebelum dihapus
    if request.POST:
        try:
            kk.nominal -= amount_item_f
            kk.save()
            item_kk.delete()
            return JsonResponse({'result':True})
        except:
            return JsonResponse({'result':False})
    return JsonResponse({'result':False,'methode':'GET'})

@login_required
def kasbesar(request):
    frm = KasBesarForm
    kb_list = KasBesar.objects.filter(created_by=request.user)

    if "q" in request.GET and request.GET["q"] is not "":
        kb_list = KasBesar.objects.filter(created_by=request.user, no_transaksi=request.GET['q'])
    if request.POST:
        frm = KasBesarForm(request.POST)
        if frm.is_valid():
            addfrm = frm.save(commit=False)
            addfrm.created_by = request.user
            addfrm.nominal = 0
            addfrm.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return redirect(reverse('core:kasbesar'))
        else:
            print(frm.errors)
            print("form tidak valid")

    context = {"frm":frm,"kasbesar":kb_list}
    return render(request,'backend/kasbesar.html', context)

@login_required
def edittemplatekb(request,pk):
    tr_obj = KasBesar.objects.get(pk=pk)
    frm = KasBesarForm(request.POST, instance=tr_obj)
    # print(frm)
    html  = render_to_string("backend/particial-modal/form-edit-kasbesar.html",{"frm":frm,"trs":tr_obj})
    data = {'html': html}
    return JsonResponse(data)

@login_required
def editkasbesar(request,pk):
    tr_obj = KasBesar.objects.get(pk=pk)
    amount_item_f = tr_obj.nominal
    if request.POST:
        frm2 = KasBesarForm(request.POST, instance=tr_obj)
        
        if frm2.is_valid():
            frm2add = frm2.save(commit=False)
            # frm2add.nominal -= amount_item_f + float(frm2add.nominal)
            frm2add.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return JsonResponse({'result':True})
        print(frm2.errors)
        print(frm2)
        return JsonResponse({'result':False})
    return redirect(reverse('core:kasbesar'))

@login_required
def deleteKasBesar(request,pk):
    kb = KasBesar.objects.get(pk=pk)
    if request.POST:
        try:
            kb.delete()
            return JsonResponse({'result':True})
        except:
            return JsonResponse({'result':False})
    return JsonResponse({'result':False,'method':'get'})
