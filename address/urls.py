from django.urls import path

from .views import getDistrict, getProvince, getVDCMunicipality, getWardNumber

urlpatterns = [
    path("getProvince/<int:country>/", getProvince, name="getState"),
    path("getDistrict/<int:province>/", getDistrict, name="getDistrict"),
    path(
        "getVDCMunicipality/<int:district>/",
        getVDCMunicipality,
        name="getVDCMunicipality",
    ),
    path("getWardNumber/<int:vdcMunicipality>/", getWardNumber, name="getWardNumber"),
]
