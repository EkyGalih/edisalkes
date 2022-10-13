from multiprocessing import context
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
#from numpy import empty, object_
from src.forms.kas_forms import KasBesarKeluarForm, KasBesarMasukForm, KasKecilDetailForm, KasKecilMasukForm, KasKecilKeluarForm, KasKecilFormEdit, TotalKasBesarKeluarForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.template.loader import get_template, render_to_string
from src.models.TransactionRecord_M import Beban, KasBesarKeluar, KasBesarMasuk, KasKecil, KasKecilDetail, Karyawan, Sales, TotalKasBesarKeluar
from django.db.models import Sum, Q
from datetime import datetime, timedelta


@login_required
def kaskecilMasuk(request):

    frm = KasKecilMasukForm
    kk_list = KasBesarKeluar.objects.filter(created_by=request.user)
    pk = "kas123"
    t_list = TotalKasBesarKeluar.objects.filter(id=pk)
    
    if t_list:
        totalKas = t_list
    else:
        totalKas = []

    if "q" in request.GET and request.GET["q"] != "":
        kk_list = KasBesarKeluar.objects.filter(
            created_by=request.user, no_kas=request.GET['q'])
    if request.POST:
        frm = KasKecilMasukForm(request.POST)
        frm2 = TotalKasBesarKeluarForm(request.POST)
        
        if frm.is_valid():
            addfrm = frm.save(commit=False)
            if frm2.is_valid():
                add2frm = frm2.save(commit=False)
                add2frm.id = pk
                add2frm.total_kas = (float(addfrm.nominal) + float(add2frm.total_kas))
                add2frm.save()
            addfrm.created_by = request.user
            addfrm.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return redirect(reverse('core:kaskecil-masuk'))
        else:
            print("form tidak valid")

    context = {"frm": frm, "kaskecilMasuk": kk_list, 'ts': totalKas}
    return render(request, 'backend/kaskecil-in.html', context)


@login_required
def kaskecilKeluar(request):
    frm = KasKecilKeluarForm
    kk_list = KasKecil.objects.filter(created_by=request.user)

    if "q" in request.GET and request.GET["q"] != "":
        kk_list = KasKecil.objects.filter(
            created_by=request.user, no_kas=request.GET['q'])

    if request.POST:
        frm = KasKecilKeluarForm(request.POST)
        if frm.is_valid():
            addfrm = frm.save(commit=False)
            addfrm.created_by = request.user
            addfrm.nominal = 0
            addfrm.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return redirect(reverse('core:kaskecil_detail_keluar', kwargs={'pk': addfrm.pk}))
        else:
            print("form tidak valid")

    context = {"frm": frm, "kaskecil": kk_list}
    return render(request, 'backend/kaskecil-out.html', context)


@login_required
def edittemplatekkMasuk(request, pk):
    kkm_obj = KasBesarMasuk.objects.get(pk=pk)
    pkt = "kas123"
    t_list = TotalKasBesarKeluar.objects.all()
    kkm = KasBesarKeluarForm(request.POST, instance=kkm_obj)
    # print(frm)
    html = render_to_string("backend/particial-modal/form-edit-kaskecil-masuk.html", {"frm": kkm, "trs": kkm_obj, "totalKas": t_list})
    data = {'html': html}
    return JsonResponse(data)


def edittemplatekkKeluar(request, pk):
    kkk_obj = kaskecilKeluar.object.get(pk=pk)
    kkk = KasKecilKeluarForm(request.POST, instance=kkk_obj)
    beban = Beban.objects.all()
    html = render_to_string(
        "backend/particial-modal/form-edit-kaskecil-keluar.html", {"frm": kkk, "trs": kkk_obj, "beban": beban})
    data = {'html': html}
    return JsonResponse(data)


@login_required
def editkaskecilMasuk(request, pk):
    kasBM_obj = KasBesarMasuk.objects.get(pk=pk)
    nominal = kasBM_obj.nominal
    totalSaldo = request.POST['total_kas']
    pkt = "kas123"
    
    if request.POST:
        frm = KasBesarMasukForm(request.POST, instance=kasBM_obj)
        frm2 = TotalKasBesarKeluarForm(request.POST)
        
        if frm.is_valid():
            addfrm = frm.save(commit=False)
            
            if nominal > addfrm.nominal:
                selisih = (float(nominal) - float(addfrm.nominal))
                total_saldo = (float(totalSaldo) - float(selisih))
            elif nominal < addfrm.nominal:
                selisih = (float(addfrm.nominal) - float(nominal))
                total_saldo = (float(totalSaldo) + float(selisih))
            
            if frm2.is_valid():
                add2frm = frm.save(commit=False)
                add2frm.id = pkt
                add2frm.total_kas = float(total_saldo)
                add2frm.save()
            
            addfrm.save()
            messages.add_message(request, messages.INFO,
                                 mark_safe('berhasil disimpan.'))
            return JsonResponse({'result': True})
        print(frm.errors)
        # print(FrmKbm)
        return JsonResponse({'result': False})
    return redirect(reverse('core:kasbesar-masuk'))


@login_required
def kaskecilDetailKeluar(request, pk):
    tr_obj = KasKecil.objects.get(pk=pk)
    kaskecil_item = KasKecilDetail.objects.filter(kk=pk)
    frm = KasKecilFormEdit(instance=tr_obj)
    frm2 = KasKecilDetailForm
    kar = Karyawan.objects.all()

    if request.POST:
        # print(request.POST["receiver_name"])
        print("berhasil masuk post")
        frm = KasKecilFormEdit(request.POST, instance=tr_obj)
        frm2 = KasKecilDetailForm(request.POST)
        if frm.is_valid():
            frmadd = frm.save(commit=False)

            if frm2.is_valid():
                frm2add = frm2.save(commit=False)
                frm2add.kk = tr_obj
                frm2add.amount = float(frm2add.quantity) * \
                    float(frm2add.unit_price)
                frmadd.nominal += frm2add.amount
                frm2add.save()
                frmadd.save()
                messages.add_message(request, messages.INFO,
                                     mark_safe('berhasil disimpan.'))
                return redirect(reverse('core:kaskecil_detail_keluar', kwargs={'pk': pk}))
            frmadd.save()
            messages.add_message(request, messages.INFO,
                                 mark_safe('berhasil disimpan.'))
            return redirect(reverse('core:kaskecil_detail_keluar', kwargs={'pk': pk}))

    context = {"trs": tr_obj, "frm2": frm2,
               "kaskecil_item": kaskecil_item, "frm": frm, "kar": kar}
    return render(request, "backend/detail-kaskecil-out.html", context)


@login_required
def edittemplateitemkk(request, pk):
    tr_obj = KasKecilDetail.objects.get(pk=pk)
    frm = KasKecilDetailForm(request.POST, instance=tr_obj)
    print(frm)
    html = render_to_string(
        "backend/particial-modal/form-edit-kaskecil-keluar.html", {"frm": frm, "trs": tr_obj})
    data = {'html': html}
    return JsonResponse(data)


@login_required
def edititemkaskecil(request, pk):
    tr_obj = KasKecilDetail.objects.get(pk=pk)
    amount_item_f = tr_obj.amount
    kk = tr_obj.kk.pk
    tr2_obj = KasKecil.objects.get(pk=kk)
    
    if request.POST:
        frm2 = KasKecilDetailForm(request.POST, instance=tr_obj)

        if frm2.is_valid():
            frm2add = frm2.save(commit=False)
            frm2add.amount = float(frm2add.quantity) * \
                float(frm2add.unit_price)
            tr2_obj.nominal = (tr2_obj.nominal -
                               amount_item_f) + float(frm2add.amount)
            frm2add.save()
            tr2_obj.save()
            messages.add_message(request, messages.INFO,
                                 mark_safe('berhasil disimpan.'))
            return JsonResponse({'result': True})
        print(frm2.errors)
        print(frm2)
        return JsonResponse({'result': False})
    return redirect(reverse('core:kaskecil_detail_keluar', kwargs={'pk': kk}))


@login_required
def deleteKasKecil(request, pk):
    kk = KasKecil.objects.get(pk=pk)
    if request.POST:
        try:
            kk.delete()
            return JsonResponse({'result': True})
        except:
            return JsonResponse({'result': False})
    return JsonResponse({'result': False, 'method': 'get'})


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
            return JsonResponse({'result': True})
        except:
            return JsonResponse({'result': False})
    return JsonResponse({'result': False, 'methode': 'GET'})


@login_required
def kasbesarMasuk(request):
    frm = KasBesarMasukForm
    kb_list = KasBesarMasuk.objects.filter(created_by=request.user)

    if "q" in request.GET and request.GET["q"] != "":
        kb_list = KasBesarMasuk.objects.filter(
            created_by=request.user, no_transaksi=request.GET['q'])
    if request.POST:
        frm = KasBesarMasukForm(request.POST)
        if frm.is_valid():
            addfrm = frm.save(commit=False)
            addfrm.created_by = request.user
            # addfrm.nominal = 0
            addfrm.save()
            messages.add_message(request, messages.INFO,
                                 mark_safe('berhasil disimpan.'))
            return redirect(reverse('core:kasbesar-masuk'))
        else:
            print(frm.errors)
            print("form tidak valid")

    context = {"frm": frm, "kasbesarMasuk": kb_list}
    return render(request, 'backend/kasbesar-in.html', context)


@login_required
def kasbesarKeluar(request):

    frm = KasBesarKeluarForm
    kb_list = KasBesarKeluar.objects.filter(created_by=request.user)
    pk = "kas123"
    t_list = TotalKasBesarKeluar.objects.filter(id=pk)

    if t_list:
        totalKas = t_list
    else:
        totalKas = []

    if "q" in request.GET and request.GET["q"] != "":
        kb_list = KasBesarKeluar.objects.filter(
            created_by=request.user, no_transaksi=request.GET['q'])
    if request.POST:
        frm = KasBesarKeluarForm(request.POST)
        frm2 = TotalKasBesarKeluarForm(request.POST)

        if frm.is_valid():
            addfrm = frm.save(commit=False)
            if frm2.is_valid():
                add2frm = frm2.save(commit=False)
                add2frm.id = pk
                add2frm.total_kas = (
                    float(addfrm.nominal) + float(add2frm.total_kas))
                add2frm.save()
            addfrm.created_by = request.user
            # addfrm.nominal = 0
            addfrm.save()
            messages.add_message(request, messages.INFO,
                                 mark_safe('berhasil disimpan.'))
            return redirect(reverse('core:kasbesar-keluar'))
        else:
            print(frm.errors)
            print("form tidak valid")

    context = {"frm": frm, "kasbesarKeluar": kb_list, "totalKas": totalKas}
    return render(request, 'backend/kasbesar-out.html', context)


@login_required
def edittemplatekbMasuk(request, pk):
    kbm_obj = KasBesarMasuk.objects.get(pk=pk)
    kbm = KasBesarMasukForm(request.POST, instance=kbm_obj)
    # print(frm)
    html = render_to_string(
        "backend/particial-modal/form-edit-kasbesar-masuk.html", {"frm": kbm, "trs": kbm_obj})
    data = {'html': html}
    return JsonResponse(data)


@login_required
def edittemplatekbKeluar(request, pk):
    kbk_obj = KasBesarKeluar.objects.get(pk=pk)
    pkt = "kas123"
    t_list = TotalKasBesarKeluar.objects.all()
    kbk = KasBesarKeluarForm(request.POST, instance=kbk_obj)
    # print(frm)
    html = render_to_string(
        "backend/particial-modal/form-edit-kasbesar-keluar.html", {"frm": kbk, "trs": kbk_obj, "totalKas": t_list})
    data = {'html': html}
    return JsonResponse(data)


@login_required
def editkasbesarKeluar(request, pk):
    kasBK_obj = KasBesarKeluar.objects.get(pk=pk)
    nominal = kasBK_obj.nominal
    totalSaldo = request.POST['total_kas']
    pkt = "kas123"
    frm = KasBesarKeluarForm(instance=kasBK_obj)
    frm2 = TotalKasBesarKeluarForm
    
    if request.POST:
        frm = KasBesarKeluarForm(request.POST, instance=kasBK_obj)
        frm2 = TotalKasBesarKeluarForm(request.POST)   
        
        if frm.is_valid():
            addfrm = frm.save(commit=False)

            if nominal > addfrm.nominal:
                selisih = (float(nominal) - float(addfrm.nominal))
                total_saldo = (float(totalSaldo) - float(selisih)) 
            elif nominal < addfrm.nominal:
                selisih = (float(addfrm.nominal) - float(nominal))
                total_saldo = (float(totalSaldo) + float(selisih))
            else:
                total_saldo = float(total_saldo)

            if frm2.is_valid():
                add2frm = frm2.save(commit=False)
                add2frm.id = pkt
                add2frm.total_kas = float(total_saldo)
                add2frm.save()
            # addfrm.nominal -= amount_item_f + float(addfrm.nominal)
            addfrm.save()
            messages.add_message(request, messages.INFO, mark_safe('berhasil disimpan.'))
            return JsonResponse({'result': True})
        
        return JsonResponse({'result': False})
    return redirect(reverse('core:kasbesar-keluar'))


@login_required
def editkasbesarMasuk(request, pk):
    kasBM_obj = KasBesarMasuk.objects.get(pk=pk)
    amount_item_f = kasBM_obj.nominal
    if request.POST:
        FrmKbm = KasBesarMasukForm(request.POST, instance=kasBM_obj)

        if FrmKbm.is_valid():
            FrmKbmadd = FrmKbm.save(commit=False)
            # FrmKbmadd.nominal -= amount_item_f + float(FrmKbmadd.nominal)
            FrmKbmadd.save()
            messages.add_message(request, messages.INFO,
                                 mark_safe('berhasil disimpan.'))
            return JsonResponse({'result': True})
        print(FrmKbm.errors)
        # print(FrmKbm)
        return JsonResponse({'result': False})
    return redirect(reverse('core:kasbesar-masuk'))


@login_required
def deleteKasBesarKeluar(request, pk):

    kbk = KasBesarKeluar.objects.get(pk=pk)

    if request.POST:
        try:
            kbk.delete()
            return JsonResponse({'result': True})
        except:
            return JsonResponse({'result': False})
    return JsonResponse({'result': False, 'method': 'get'})


@login_required
def deleteKasBesarMasuk(request, pk):

    kbm = KasBesarMasuk.objects.get(pk=pk)

    if request.POST:
        try:
            kbm.delete()
            return JsonResponse({'result': True})
        except:
            return JsonResponse({'result': False})
    return JsonResponse({'result': False, 'method': 'get'})
