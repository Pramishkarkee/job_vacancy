from datetime import datetime

from address.forms import AddressFormset
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from jobs.models import Vacancy
from PIL import Image
from professional.forms import ExperienceFormset, QualificationFormset
from professional.models import Category, Experience, Qualification, Skill

from .decorators import check_permission
from .forms import ApplicantRegistrationForm, ProviderRegistrationForm, UserCreationForm
from .models import Applicant, Provider


def about(request):
    return HttpResponse("About testing")


def userSignup(request, profile_type):
    context = {}
    if request.method == "POST":
        userCreateForm = UserCreationForm(request.POST, request.FILES)
        print("------------------------------------------------------------------")
        print(userCreateForm.errors)
        print("------------------------------------------------------------------")
        if userCreateForm.is_valid():
            new_user = userCreateForm.save(commit=False)
            if profile_type == "applicant":
                new_user.profile_type = "A"
            elif profile_type == "provider":
                new_user.profile_type = "P"
            new_user.save()
            profile_photo = Image.open(new_user.profile_photo.path)
            resized_image = profile_photo.resize((128, 128), Image.ANTIALIAS)
            resized_image.save(new_user.profile_photo.path)

            username = userCreateForm.cleaned_data["username"]
            raw_password = userCreateForm.cleaned_data["password1"]
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if profile_type == "applicant":
                return redirect("home")
            elif profile_type == "provider":
                return redirect("provider_registration")
    else:
        userCreateForm = UserCreationForm()
    context = {
        "form": userCreateForm,
        "profile_type": profile_type,
    }
    return render(request, "records/signup.html", context)


@login_required(login_url="login")
@check_permission(profiletype="A")
def applicantSignup(request):
    if request.user.is_registered:
        return redirect("search")

    context = {}
    if request.method == "POST":
        applicantForm = ApplicantRegistrationForm(request.POST, request.FILES)
        temporaryAddressForm = AddressFormset(request.POST, prefix="temporary_address")
        permanentAddressForm = AddressFormset(request.POST, prefix="permanent_address")
        experienceForm = ExperienceFormset(request.POST, prefix="experience")
        qualificationForm = QualificationFormset(request.POST, prefix="qualification")
        print(applicantForm.errors)
        print(temporaryAddressForm.errors)
        print(permanentAddressForm.errors)
        print(experienceForm.errors)
        print(qualificationForm.errors)
        if (
            applicantForm.is_valid()
            and temporaryAddressForm.is_valid()
            and permanentAddressForm.is_valid()
            and experienceForm.is_valid()
            and qualificationForm.is_valid()
        ):

            applicant = applicantForm.save(commit=False)
            temporaryAddress = temporaryAddressForm.cleaned_data[0]["ward_number"]
            permanentAddress = permanentAddressForm.cleaned_data[0]["ward_number"]
            skills_field = applicantForm.cleaned_data["addedSkill"]
            category_field = applicantForm.cleaned_data["added_category"]

            print(temporaryAddress)
            print(permanentAddress)
            user = request.user
            applicant.id = user
            applicant.temporary_address = temporaryAddress
            applicant.permanent_address = permanentAddress
            qualification = qualificationForm[0].save(commit=False)
            db_qualification = Qualification.objects.filter(
                level=qualification.level, field=qualification.field
            )
            if db_qualification:
                applicant.qualification = db_qualification.get()
                print("Already Exists")
            else:
                qualification.save()
                applicant.qualification = qualification
                print("Created New")
            applicant.save()
            for form in experienceForm:
                role = form.cleaned_data["role"]
                no_of_years = form.cleaned_data["no_of_years"]

                experience_entries = Experience.objects.filter(
                    role=role, no_of_years=no_of_years
                )

                if experience_entries:
                    applicant.experience.add(experience_entries.get())
                else:
                    new_experience = Experience(no_of_years=no_of_years, role=role)
                    new_experience.save()
                    applicant.experience.add(new_experience)
            applicant.id.is_registered = True
            applicant.save()

            applicantForm.save_m2m()
            if skills_field:
                new_skill = Skill.objects.get_or_create(name=skills_field)
                applicant.skills.add(new_skill[0])

            if category_field:
                new_category = Category.objects.get_or_create(name=category_field)
                applicant.interested_categories.add(new_category[0])

            applicant.save()
            return redirect("home")
    else:
        applicantForm = ApplicantRegistrationForm()
        temporaryAddressForm = AddressFormset(prefix="temporary_address")
        permanentAddressForm = AddressFormset(prefix="permanent_address")
        experienceForm = ExperienceFormset(prefix="experience")
        qualificationForm = QualificationFormset(prefix="qualification")
    context = {
        "form": applicantForm,
        "temporary_address": temporaryAddressForm,
        "permanent_address": permanentAddressForm,
        "experience": experienceForm,
        "qualification": qualificationForm,
    }
    return render(request, "records/register.html", context)


@login_required(login_url="login")
@check_permission(profiletype="P")
def providerSignup(request):
    if request.user.is_registered:
        return redirect("search")

    context = {}
    if request.method == "POST":
        print(request.POST)
        providerForm = ProviderRegistrationForm(request.POST)
        addressForm = AddressFormset(request.POST, prefix="address")
        print(providerForm.errors)
        if providerForm.is_valid():
            provider = providerForm.save(commit=False)
            address = addressForm.cleaned_data[0]["ward_number"]
            category_field = providerForm.cleaned_data["added_category"]

            user = request.user
            provider.id = user
            provider.address = address
            provider.is_registered = True
            provider.save()
            providerForm.save_m2m()
            if category_field:
                new_category = Category.objects.get_or_create(name=category_field)
                provider.categories_covered.add(new_category[0])
            provider.save()
            return redirect("home")
    else:
        providerForm = ProviderRegistrationForm()
        addressForm = AddressFormset(prefix="address")
    context = {"form": providerForm, "address": addressForm}
    return render(request, "records/register.html", context)


@login_required(login_url="login")
@check_permission(profiletype="A")
def applicantUpdate(request):
    context = {}
    user = request.user
    applicant = Applicant.objects.get(id=user)
    applicantForm = ApplicantRegistrationForm(
        request.POST or None, request.FILES or None, instance=applicant
    )

    print(applicant.temporary_address.vdc_municipality.district.province.country)
    temporaryAddressForm = AddressFormset(
        request.POST or None, prefix="temporary_address"
    )
    permanentAddressForm = AddressFormset(
        request.POST or None, prefix="permanent_address"
    )
    qualificationForm = QualificationFormset(
        request.POST or None,
        prefix="qualification",
        initial=[
            {
                "level": applicant.qualification.level,
                "field": applicant.qualification.field,
            }
        ],
    )
    experienceForm = ExperienceFormset(request.POST or None, prefix="experience")

    if request.method == "POST":
        print(applicantForm.errors)
        print(temporaryAddressForm.errors)
        print(permanentAddressForm.errors)
        print(experienceForm.errors)
        print(qualificationForm.errors)
        if (
            applicantForm.is_valid()
            and temporaryAddressForm.is_valid()
            and permanentAddressForm.is_valid()
            and experienceForm.is_valid()
            and qualificationForm.is_valid()
        ):
            applicant = applicantForm.save(commit=False)
            temporaryAddress = temporaryAddressForm.cleaned_data[0]["ward_number"]
            permanentAddress = permanentAddressForm.cleaned_data[0]["ward_number"]
            skills_field = applicantForm.cleaned_data["addedSkill"]
            category_field = applicantForm.cleaned_data["added_category"]

            print(temporaryAddress)
            print(permanentAddress)
            user = request.user
            applicant.id = user
            applicant.temporary_address = temporaryAddress
            applicant.permanent_address = permanentAddress
            qualification = qualificationForm[0].save(commit=False)
            db_qualification = Qualification.objects.filter(
                level=qualification.level, field=qualification.field
            )
            if db_qualification:
                applicant.qualification = db_qualification.get()
                print("Already Exists")
            else:
                qualification.save()
                applicant.qualification = qualification
                print("Created New")
            applicant.save()

            previous_experiences = applicant.experience.all()
            for previous_experience in previous_experiences:
                applicant.experience.remove(previous_experience)

            for form in experienceForm:
                role = form.cleaned_data["role"]
                no_of_years = form.cleaned_data["no_of_years"]

                experience_entries = Experience.objects.filter(
                    role=role, no_of_years=no_of_years
                )

                if experience_entries:
                    applicant.experience.add(experience_entries.get())
                else:
                    new_experience = Experience(no_of_years=no_of_years, role=role)
                    new_experience.save()
                    applicant.experience.add(new_experience)
            applicant.save()

            applicant.id.is_registered = True
            applicantForm.save_m2m()

            if skills_field:
                new_skill = Skill.objects.get_or_create(name=skills_field)
                applicant.skills.add(new_skill[0])

            if category_field:
                new_category = Category.objects.get_or_create(name=category_field)
                applicant.interested_categories.add(new_category[0])

            applicant.save()
            return redirect("home")

    context = {
        "form": applicantForm,
        "temporary_address": temporaryAddressForm,
        "permanent_address": permanentAddressForm,
        "qualification": qualificationForm,
        "experience": experienceForm,
        "applicant": applicant,
    }
    return render(request, "records/register.html", context)


@login_required(login_url="login")
@check_permission(profiletype="P")
def providerUpdate(request):
    context = {}
    user = request.user
    provider = Provider.objects.get(id=user)
    print(provider)

    providerForm = ProviderRegistrationForm(request.POST or None, instance=provider)
    addressForm = AddressFormset(request.POST or None, prefix="address")

    if request.method == "POST":
        if providerForm.is_valid():
            provider = providerForm.save(commit=False)
            address = addressForm.cleaned_data[0]["ward_number"]
            category_field = providerForm.cleaned_data["added_category"]

            user = request.user
            provider.id = user
            provider.address = address
            provider.is_registered = True
            provider.save()
            providerForm.save_m2m()
            if category_field:
                new_category = Category.objects.get_or_create(name=category_field)
                provider.categories_covered.add(new_category[0])
            provider.save()
            return redirect("home")

    context = {"form": providerForm, "address": addressForm, "provider": provider}
    return render(request, "records/register.html", context)


def list_applicant_details(request, applicant_id):
    try:
        applicant = Applicant.objects.get(id=applicant_id)
        context = {"applicant": applicant}
    except Applicant.DoesNotExist:
        raise Http404("Applicant does not exist")
    return render(request, "records/applicant-detail-list.html", context)


def list_provider_details(request, provider_id):
    try:
        provider = Provider.objects.get(id=provider_id)
        vacancies = Vacancy.objects.filter(
            job__provider=provider, deadline_date__gt=datetime.today()
        )
        context = {"provider": provider, "vacancies": vacancies}
    except Provider.DoesNotExist:
        raise Http404("Provider does not exist")
    return render(request, "records/provider-detail-list.html", context)
