import datetime

from crispy_forms.bootstrap import Field, InlineRadios

# from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset  # Field,; MultiField,
from crispy_forms.layout import HTML, Div, Layout, MultiWidgetField, Row, Submit
from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from professional.dynamic_layout_object_formset import DynamicFormset
from professional.models import Category, Skill

from .choices import EMPLOYMENT_STATUS_CHOICES, GENDER_CHOICES
from .layoutObjectFormset import Formset
from .models import Applicant, Provider, User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
            "email",
            "contact_number",
            "profile_photo",
            # "profile_type",
        ]

    first_name = forms.CharField(label="First Name")
    middleName = forms.CharField(label="Middle Name", required=False)
    last_name = forms.CharField(label="Last Name", required=False)

    username = forms.CharField(label="Username")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    email = forms.CharField(widget=forms.EmailInput(), label="Email Address")
    contact_number = forms.IntegerField(
        widget=forms.TextInput(), label="Contact Number"
    )
    profile_photo = forms.ImageField(label="Profile Photo", required=False)

    # profile_type = forms.ChoiceField(
    #     choices=PROFILE_TYPE_CHOICES, label="Profile Type")

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "register-form"
        self.helper.layout = Layout(
            Div(
                Row(
                    Field("username", css_class="form-input col-lg-12 mb-0 pt-2 py-1"),
                    css_class="form-row",
                ),
                Row(
                    Field(
                        "first_name", css_class="form-input col-md-12 mb-0 pt-2 py-1"
                    ),
                    # Field('middleName',
                    # css_class='form-input col-md-6 mb-0 pt-2 py-1'),
                    Field("last_name", css_class="form-input col-md-12 mb-0 pt-2 py-1"),
                    css_class="form-row",
                ),
                Row(
                    Field("password1", css_class="form-input col-md-12 mb-0 pt-2 py-1"),
                    Field("password2", css_class="form-input col-md-12 mb-0 pt-2 py-1"),
                    css_class="form-row",
                ),
                Row(
                    Field("email", css_class="form-input col-lg-12 mb-0 pt-2 py-1"),
                    css_class="form-row",
                ),
                Row(
                    Field(
                        "contact_number",
                        css_class="form-input col-md-12 mb-0 pt-2 py-1",
                    ),
                ),
                Row(
                    Field("profile_photo", css_class="form-input col-md-12"),
                ),
                css_class="form-group",
            ),
            # Row(
            #     Field("profile_type", css_class="form-control"),
            #     css_class="form-row",
            # ),
            Submit("submit", "Sign Up", css_class="submit btn btn-dark"),
        )

        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            print("error")
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            print("saved")
        return user


# ApplicantFormset = inlineformset_factory(
#     Qualification, Applicant, form=ApplicantRegistrationForms,
#     fields=['level', 'field'],
#     can_delete=True
# )


class ApplicantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = [
            "id",
            "temporary_address",
            "permanent_address",
            "experience",
            "qualification",
        ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect(), label="Gender"
    )

    current_year = datetime.date.today().year
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.SelectDateWidget(
            years=[i for i in range(current_year, current_year - 150, -1)],
            empty_label=("(Select Year)", "(Select Month)", "(Select Day)"),
        ),
    )

    # qualification = forms.ModelChoiceField(
    #     queryset=Qualification.objects.all(),
    #     widget=forms.Select(),
    #     label="qualification",
    # )

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    addedSkill = forms.CharField(label="Others, Please specify.", required=False)

    cv = forms.FileField(label="Resume")

    supporting_document = forms.FileField(label="Supporting Document", required=False)

    profile_links = SimpleArrayField(forms.CharField(max_length=100))

    interested_categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label="Interested Category",
        widget=forms.CheckboxSelectMultiple,
    )
    added_category = forms.CharField(label="Others, Please specify.", required=False)

    employment_status = forms.ChoiceField(
        choices=EMPLOYMENT_STATUS_CHOICES,
        widget=forms.RadioSelect(),
        label="Employment Status",
    )

    def __init__(self, *args, **kwargs):
        super(ApplicantRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "register-form"
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    "General",
                    Row(
                        MultiWidgetField(
                            "date_of_birth",
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
                        InlineRadios("gender", css_class="form-radio-group"),
                        css_class="form-row",
                    ),
                ),
                HTML("<br>"),
                Fieldset(
                    "Temporary Address",
                    Formset("temporary_address"),
                    # css_class="tab",
                ),
                HTML("<br>"),
                Fieldset(
                    "Permanent Address",
                    Formset("permanent_address"),
                    # css_class="tab",
                ),
                # Row(
                #     Field(
                # "qualification", css_class="form-input col-lg-12 mb-0 pt-2 py-1"
                #     ),
                #     css_class="form-row",
                # ),
                HTML("<br>"),
                Fieldset(
                    "Qualification",
                    Formset("qualification"),
                    # css_class="tab",
                ),
                HTML("<br>"),
                # Fieldset('<p class="h4 pb-3">Qualification Information</p>',
                #          Formset('qualification'), css_class="tab"),
                Fieldset(
                    "",
                    Field("skills", css_class="form-check-input col-md-12"),
                    Field("addedSkill", css_class="form-input col-md-6 mb-0"),
                ),
                Fieldset(
                    # Field("experience",
                    # css_class="select-list col-auto mb-0 pt-2 py-1"),
                    "Experience",
                    Row(
                        DynamicFormset("experience"),
                        css_class="form-row fix col-md-6 mb-0 pt-2 py-1",
                    ),
                ),
                # Row(
                #     # Field("experience",
                #     # css_class="select-list col-auto mb-0 pt-2 py-1"),
                #     Fieldset("Experience", DynamicFormset("experience")),
                #     css_class="form-row col-auto mb-0 pt-2 py-1",
                # ),
                HTML("<br>"),
                Fieldset(
                    "Documents",
                    Row(
                        Field("cv", css_class="select-list col-auto mb-0 pt-2 py-1"),
                        css_class="form-row",
                    ),
                    Row(
                        Field(
                            "supporting_document",
                            css_class="select-list col-auto mb-0 pt-2 py-1",
                        ),
                        css_class="form-row",
                    ),
                    Row(
                        Field(
                            "profile_links",
                            css_class="select-list col-auto mb-0 pt-2 py-1",
                        ),
                        css_class="form-row",
                    ),
                ),
                HTML("<br>"),
                Fieldset(
                    "Current Status",
                    Fieldset(
                        "",
                        Field(
                            "interested_categories",
                            css_class="form-check-input col-auto mb-0 pt-2 py-1",
                        ),
                        Field("added_category", css_class="form-input col-md-6 mb-0"),
                        css_class="mb-3",
                    ),
                    Row(
                        InlineRadios("employment_status", css_class="form-radio-group"),
                        css_class="form-row",
                    ),
                ),
                Submit("submit", "Register", css_class="submit btn btn-dark"),
                css_class="form-group",
            ),
        )


# class ProviderCreationForm(forms.ModelForm):
#     class Meta:
#         model = Provider
#         exclude = ['id']
#
#     address = forms.ModelChoiceField(queryset=WardNumber.objects.all(),
#       label="Company Address")
#
#     website = forms.URLField(max_length=255, label="Company Websites")
#
#     category_covered = model.Mode


class ProviderRegistrationForm(forms.ModelForm):
    class Meta:
        model = Provider
        exclude = ["id", "address"]

    website = forms.URLField(required=False)

    categories_covered = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label="Category",
        widget=forms.CheckboxSelectMultiple,
    )
    added_category = forms.CharField(label="Others, Please specify.", required=False)
    description = forms.CharField(widget=forms.Textarea, label="Description")

    def __init__(self, *args, **kwargs):
        super(ProviderRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "register-form"
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    "Address",
                    Formset("address"),
                    # css_class="tab",
                ),
                Row(
                    Field("website", css_class="select-list col-auto mb-0 pt-2 py-1"),
                    css_class="form-row",
                ),
                Fieldset(
                    "",
                    Field(
                        "categories_covered",
                        css_class="select-list col-auto mb-0 pt-2 py-1",
                    ),
                    Field("added_category", css_class="form-input col-md-6 mb-0"),
                    css_class="mb-3",
                ),
                Row(
                    Field(
                        "description", css_class="select-list col-auto mb-0 pt-2 py-1"
                    ),
                    css_class="form-row",
                ),
                Submit("submit", "Register", css_class="submit btn"),
            )
        )
