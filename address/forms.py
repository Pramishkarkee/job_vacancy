from django import forms
from django.forms.formsets import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field

from .models import Country, District, Province, VDCMunicipality, WardNumber


class AddressForm(forms.Form):
    ward_number = forms.ModelChoiceField(
        queryset=WardNumber.objects.all(),
        widget=forms.Select(),
        label="Ward Number",
        empty_label="(Select Ward Number)",
    )
    vdc_municipality = forms.ModelChoiceField(
        queryset=VDCMunicipality.objects.all(),
        widget=forms.Select(),
        label="VDC/Municipality",
        empty_label="(Select VDC/Municipality)",
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        widget=forms.Select(),
        label="District",
        empty_label="(Select District)",
    )
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        widget=forms.Select(),
        label="Province",
        empty_label="(Select Province)",
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=forms.Select(),
        label="Country",
        empty_label="(Select Country)",
    )

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.helper.form_class =
        self.helper.layout = Layout(
            Div(
                Row(
                    Field("country", css_class="select-list col-auto mb-0 pt-2 py-1"),
                    css_class="form-row",
                ),
                Row(
                    Field("province", css_class="select-list col-auto mb-0 pt-2 py-1"),
                    Field("district", css_class="select-list col-auto mb-0 pt-2 py-1"),
                    css_class="form_row",
                ),
                Row(
                    Field(
                        "vdc_municipality",
                        css_class="select-list col-auto mb-0 pt-2 py-1",
                    ),
                    Field(
                        "ward_number", css_class="form-input col-auto mb-0 pt-2 py-1"
                    ),
                    css_class="form-row",
                ),
                # css_class="tab-address",
            )
        )


AddressFormset = formset_factory(AddressForm, max_num=1)
