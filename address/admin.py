from django.contrib import admin

from address.models import Country, Province, District, VDCMunicipality, WardNumber

admin.site.register(Country)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(VDCMunicipality)
admin.site.register(WardNumber)
