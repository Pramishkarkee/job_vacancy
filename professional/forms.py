import re

from django import forms
from django.forms.formsets import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Submit,
    Row,
    Div,
)
from crispy_forms.bootstrap import Field

from .models import Qualification, Skill, Category, Experience
from .choices import QUALIFICATION_LEVEL_CHOICES


class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        exclude = []

    current_fields = list(
        set(list(Qualification.objects.all().values_list("field", flat=True)))
    )
    fields_choices = (("", "(Select Field)"),) + tuple(
        [(field, field) for field in current_fields]
    )

    level = forms.ChoiceField(
        choices=QUALIFICATION_LEVEL_CHOICES,
        widget=forms.Select(),
        label="Academic Level",
    )

    field = forms.ChoiceField(
        choices=fields_choices,
        widget=forms.Select(),
        label="Major",
    )

    def __init__(self, *args, **kwargs):
        super(QualificationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "register-form"
        self.helper.layout = Layout(
            Div(
                Row(
                    Field(
                        "level",
                        css_class="select-list col-auto mb-0 pt-2 py-1",
                    ),
                    Field(
                        "field",
                        css_class="select-list col-auto mb-0 pt-2 py-1",
                    ),
                    css_class="form_row",
                ),
            )
        )


class QualificationSearchForm(forms.Form):
    level = forms.ChoiceField(
        widget=forms.Select(), choices=QUALIFICATION_LEVEL_CHOICES, required=False
    )

    Category = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=Category.objects.all(),
        required=False,
        empty_label="(Select Category)",
    )

    Skill = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=Skill.objects.all(),
        required=False,
        empty_label="(Select Skill)",
    )

    def __init__(self, *args, **kwargs):
        super(QualificationSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
        self.helper.form_method = "POST"
        self.helper.form_tag = True
        self.helper.layout = Layout(
            # Div(
            #     Row(
            #         Field("level", css_class="select-list col-auto mb-0 pt-2 py-1"),
            #         css_class="form-row",
            #     ),
            #     Row(
            #         Field("Category", css_class="select-list col-auto mb-0
            #  pt-2 py-1"),
            #         css_class="form-row",
            #     ),
            #     Row(
            #         Field("Skill", css_class="select-list col-auto mb-0 pt-2 py-1"),
            #         css_class="form-row",
            #     ),
            #     css_class="form-group",
            # )
            Div(
                Div(
                    Field("level", css_class="select-list col-auto"),
                    css_class="col-12 col-sm-6 col-md-6 col-lg-3 mb-4 mb-lg-0",
                ),
                Div(
                    Field("Category", css_class="select-list col-auto"),
                    css_class="col-12 col-sm-6 col-md-6 col-lg-3 mb-4 mb-lg-0",
                ),
                Div(
                    Field("Skill", css_class="select-list col-auto"),
                    css_class="col-12 col-sm-6 col-md-6 col-lg-3 mb-4 mb-lg-0",
                ),
                Div(
                    Submit(
                        "Submit",
                        "Search Applicants",
                        css_class="btn btn-primary btn-lg btn-block text-white"
                        " btn-search col-auto fix-margin-form",
                    ),
                    css_class="col-12 col-sm-6 col-md-6 col-lg-3 mb-4 mb-lg-0",
                ),
                css_class="row",
            )
            # Div(
            #     Row(
            #         Field("level", css_class="select-list col-auto mb-0 pt-2 py-1"),
            #         css_class="form-row",
            #     ),
            #     Row(
            #         Field("Category", css_class="select-list col-auto mb-0
            # pt-2 py-1"),
            #         css_class="form-row",
            #     ),
            #     Row(
            #         Field("Skill", css_class="select-list col-auto mb-0 pt-2 py-1"),
            #         css_class="form-row",
            #     ),
            #     css_class="form-group",
            # )
        )


class ExperienceForm(forms.Form):
    current_roles = list(
        set(list(Experience.objects.all().values_list("role", flat=True)))
    )
    roles_choices = (("", "(Select Role)"),) + tuple(
        [(role, role) for role in current_roles]
    )
    print(roles_choices)
    role = forms.ChoiceField(
        widget=forms.Select(),
        choices=roles_choices,
        label="Role",
    )
    no_of_years = forms.IntegerField(widget=forms.TextInput(), label="No. of Years")

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)

        formtag_prefix = re.sub("-[0-9]+$", "", kwargs.get("prefix", ""))

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Field("no_of_years", css_class="form-input col-12 mb-0 pt-2 py-1"),
                    Field("role", css_class="select-list col-12 mb-0 pt-2 py-1"),
                    # css_class="form-row",
                    css_class="form-row formset-row-{}".format(formtag_prefix),
                ),
            )
        )


ExperienceFormset = formset_factory(ExperienceForm, extra=1, max_num=5, min_num=1)
JobExperienceFormset = formset_factory(ExperienceForm, max_num=1)
QualificationFormset = formset_factory(QualificationForm, max_num=1)
