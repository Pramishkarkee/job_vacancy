from django import forms
from .models import Job, Vacancy
from professional.models import Category, Skill
from professional.choices import QUALIFICATION_LEVEL_CHOICES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Submit,
    Row,
    # Column,
    Div,
    # Field,
    # HTML,
    Fieldset,
    # MultiField,
    MultiWidgetField,
)
from crispy_forms.bootstrap import Field  # , InlineRadios
from datetime import datetime
from records.layoutObjectFormset import Formset


class JobRegistrationForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ["provider", "min_qualification", "min_required_experience"]

    name = forms.CharField(label="Job Name")

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="(Select Category)"
    )

    position = forms.CharField(label="Opened Position")

    # min_qualification = forms.ModelChoiceField(queryset=Qualification.objects.all(),
    #                                            label='Minimum Qualification')

    # min_required_experience = forms.ModelMultipleChoiceField(
    #                               queryset=Experience.objects.all(),
    #                               label='Minimum Experienced'
    # )

    required_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Required Skills",
    )
    added_skill = forms.CharField(label="Others, Please specify.", required=False)

    description = forms.CharField(widget=forms.Textarea, label="Job Description")

    allowance = forms.IntegerField(
        widget=forms.TextInput, required=False, label="Allowance"
    )

    def __init__(self, *args, **kwargs):
        super(JobRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "register-form"
        self.helper.layout = Layout(
            Div(
                Row(
                    Field("name", css_class="form-input col-auto mb-0 pt-2 py-1"),
                    css_class="form-row",
                ),
                Row(
                    Field("category", css_class="select-list col-auto mb-0 pt-2 py-1"),
                    css_class="form-row",
                ),
                Row(
                    Field("position", css_class="form-input col-auto mb-0 pt-2 py-1"),
                    css_class="form-row",
                ),
                # Row(
                #     Field('min_qualification',
                #     css_class='select-list col-auto mb-0 pt-2 py-1'),
                #     css_class='form-row',
                # ),
                # Row(
                #     Field('min_required_experience',
                #     css_class='form-input col-auto mb-0 pt-2 py-1'),
                #     css_class='form-row',
                # ),
                Fieldset(
                    "Minimum Qualification",
                    Formset("qualification"),
                    # css_class="tab",
                ),
                Fieldset(
                    "Minimum Experience",
                    Formset("experience"),
                    # css_class="tab",
                ),
                Fieldset(
                    "",
                    Field(
                        "required_skills",
                        css_class="select-list col-auto mb-0 pt-2 py-1",
                    ),
                    Field("added_skill", css_class="form-input col-md-6 mb-0"),
                    css_class="mb-3",
                ),
                Row(
                    Field(
                        "description", css_class="select-list col-auto mb-0 pt-2 py-1"
                    ),
                    css_class="form-row",
                ),
                Row(
                    Field("allowance", css_class="form-input col-auto mb-0 pt-2 py-1"),
                    css_class="form-row",
                ),
                Submit("submit", "Submit", css_class="submit btn"),
            )
        )


class VacancyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ["Applicant", "job"]

    # job = forms.ModelChoiceField(label='Vacancy for jobs', queryset=Job.objects.all())

    is_part_time = forms.BooleanField(label="Part Time")

    num_vacancies = forms.IntegerField(widget=forms.TextInput, label="No of Vacancies")

    notice_image = forms.FileField(label="Announcement Notice Image")

    announced_date = forms.DateField(
        widget=forms.SelectDateWidget(), label="Announced Date", initial=datetime.now
    )

    deadline_date = forms.DateField(
        widget=forms.SelectDateWidget(),
        label="Application Deadline",
        initial=datetime.now,
    )

    def __init__(self, *args, **kwargs):

        super(VacancyRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.fields["job"].queryset = Job.objects.filter(provider=provider)
        self.helper.form_tag = True
        self.helper.form_class = "register-form"
        self.helper.layout = Layout(
            Div(
                # Row(
                #     Field("job", css_class="select-list col-auto mb-0 pt-2 py-1"),
                #     css_class="form-row",
                # ),
                Row(
                    Field(
                        "num_vacancies", css_class="form-input col-auto mb-0 pt-2 py-1"
                    ),
                    css_class="form-row",
                ),
                Row(
                    Field(
                        "notice_image", css_class="form-input col-auto mb-0 pt-2 py-1"
                    ),
                    css_class="form-row",
                ),
                Row(
                    Field("is_part_time", css_class="form-radio-group"),
                    css_class="form-row",
                ),
                # Row(
                #     Field('announced_date',
                #     css_class='select-list col-auto mb-0 pt-2 py-1'),
                #     css_class='form-row',
                # ),
                # Row(
                #     Field('deadline_date',
                #     css_class='select-list col-auto mb-0 pt-2 py-1'),
                #     css_class='form-row',
                # ),
                Row(
                    MultiWidgetField(
                        "announced_date",
                        css_class="form-input col-lg-12 mb-0 pt-2 py-1",
                        attrs=(
                            {
                                "style": """width: 30%;
                                            margin: 4px;
                                            display: inline-block;"""
                            }
                        ),
                    ),
                    css_class="form-row",
                ),
                Row(
                    MultiWidgetField(
                        "deadline_date",
                        css_class="form-input col-lg-12 mb-0 pt-2 py-1",
                        attrs=(
                            {
                                "style": """width: 30%;
                                            margin: 4px;
                                            display: inline-block;"""
                            }
                        ),
                    ),
                    css_class="form-row",
                ),
                Submit("submit", "Submit", css_class="submit btn"),
                css_class="form-group",
            )
        )


class JobSearchForm(forms.Form):

    Category = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=Category.objects.all(),
        required=False,
        label="",
        empty_label="(Select Category)",
    )

    Level = forms.ChoiceField(
        widget=forms.Select(),
        choices=QUALIFICATION_LEVEL_CHOICES,
        required=False,
        label="",
    )

    Skill = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=Skill.objects.all(),
        required=False,
        label="",
        empty_label="(Select Skill)",
    )

    def __init__(self, *args, **kwargs):
        super(JobSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.add_input()
        self.helper.form_method = "POST"
        self.helper.form_tag = True
        self.helper.form_class = "search-jobs-form"
        self.helper.layout = Layout(
            Div(
                Div(
                    Field("Level", css_class="select-list col-auto"),
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
                        "Search Job",
                        css_class="btn btn-primary btn-lg btn-block"
                        " text-white btn-search col-auto",
                    ),
                    css_class="col-12 col-sm-6 col-md-6 col-lg-3 mb-4 mb-lg-0",
                ),
                css_class="row mb-5",
            )
        )
