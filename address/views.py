from django.views.decorators.http import require_safe
from django.http import JsonResponse

from .models import WardNumber, VDCMunicipality, District, Province


@require_safe
def getWardNumber(request, vdcMunicipality):
    if request.user.is_authenticated:
        wardNumbers = WardNumber.objects.filter(
            vdc_municipality=vdcMunicipality
        ).values_list("id", "ward_number")
        return JsonResponse(list(wardNumbers), safe=False)
    return JsonResponse({"status": False, "message": "Not logged in yet"}, status=400)


@require_safe
def getVDCMunicipality(request, district):
    if request.user.is_authenticated:
        vdcMunicipalities = VDCMunicipality.objects.filter(
            district=district
        ).values_list("id", "name")
        return JsonResponse(list(vdcMunicipalities), safe=False)
    return JsonResponse({"status": False, "message": "Not logged in yet"}, status=400)


@require_safe
def getDistrict(request, province):
    if request.user.is_authenticated:
        districts = District.objects.filter(province=province).values_list("id", "name")
        return JsonResponse(list(districts), safe=False)
    return JsonResponse({"status": False, "message": "Not logged in yet"}, status=400)


@require_safe
def getProvince(request, country):
    if request.user.is_authenticated:
        provinces = Province.objects.filter(country=country).values_list("id", "name")
        return JsonResponse(list(provinces), safe=False)
    return JsonResponse({"status": False, "message": "Not logged in yet"}, status=400)
