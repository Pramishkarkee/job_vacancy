from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render
from professional.forms import JobExperienceFormset, QualificationFormset
from professional.models import Experience, Qualification, Skill
from records.decorators import check_permission
from records.models import Applicant, Provider

from .forms import JobRegistrationForm, JobSearchForm, VacancyRegistrationForm
from .models import Job, Vacancy


@login_required(login_url="login")
@check_permission(profiletype="P")
def jobRegister(request):
    if request.method == "POST":

        jobForm = JobRegistrationForm(request.POST)
        qualificationForm = QualificationFormset(request.POST, prefix="qualification")
        experienceForm = JobExperienceFormset(request.POST, prefix="experience")


        if (
            jobForm.is_valid()
            and qualificationForm.is_valid()
            and experienceForm.is_valid()
        ):
            job = jobForm.save(commit=False)
            user = request.user
            provider = Provider.objects.get(id=user)
            job.provider = provider
            skills_field = jobForm.cleaned_data["added_skill"]

            qualification = qualificationForm[0].save(commit=False)
            db_qualification = Qualification.objects.filter(
                level=qualification.level, field=qualification.field
            )
            if db_qualification:
                job.min_qualification = db_qualification.get()
                print("Already Exists")
            else:
                qualification.save()
                job.min_qualification = qualification
                print("Created New")

            job.save()

            role = experienceForm.cleaned_data[0]["role"]
            no_of_years = experienceForm.cleaned_data[0]["no_of_years"]

            experience_entries = Experience.objects.filter(
                role=role, no_of_years=no_of_years
            )

            if experience_entries:
                print(experience_entries)
                job.min_required_experience.add(experience_entries.get())
            else:
                new_experience = Experience(no_of_years=no_of_years, role=role)
                new_experience.save()
                job.min_required_experience.add(new_experience)

            jobForm.save_m2m()
            if skills_field:
                new_skill = Skill.objects.get_or_create(name=skills_field)
                job.required_skills.add(new_skill[0])
            job.save()
            return redirect("home")
    else:
        jobForm = JobRegistrationForm()
        qualificationForm = QualificationFormset(prefix="qualification")
        experienceForm = JobExperienceFormset(prefix="experience")
        context = {
            "form": jobForm,
            "qualification": qualificationForm,
            "experience": experienceForm,
        }
        return render(request, "records/register.html", context)


@login_required(login_url="login")
@check_permission(profiletype="P")
def vacancyRegister(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == "POST":
        print(request.POST)
        vacancyForm = VacancyRegistrationForm(request.POST, request.FILES)
        print(vacancyForm.errors)
        if vacancyForm.is_valid():
            vacancy = vacancyForm.save(commit=False)
            vacancy.job = job
            vacancy.save()
            return redirect("home")

    else:
        vacancyForm = VacancyRegistrationForm()
        context = {"form": vacancyForm}
        return render(request, "records/register.html", context)


@login_required(login_url="login")
@check_permission(profiletype="P")
def updateJob(request, id):
    job = Job.objects.get(pk=id)
    jobForm = JobRegistrationForm(request.POST or None, instance=job)
    qualificationForm = QualificationFormset(
        request.POST or None,
        initial=[
            {"level": job.min_qualification.level, "field": job.min_qualification.field}
        ],
        prefix="qualification",
    )
    experienceForm = JobExperienceFormset(
        request.POST or None,
        initial=[
            {
                "role": job.min_required_experience.all()[0].role,
                "no_of_years": job.min_required_experience.all()[0].no_of_years,
            }
        ],
        prefix="experience",
    )
    if (
        jobForm.is_valid()
        and qualificationForm.is_valid()
        and experienceForm.is_valid()
    ):
        job = jobForm.save(commit=False)
        user = request.user
        provider = Provider.objects.get(id=user)
        job.provider = provider
        skills_field = jobForm.cleaned_data["added_skill"]

        qualification = qualificationForm[0].save(commit=False)
        db_qualification = Qualification.objects.filter(
            level=qualification.level, field=qualification.field
        )
        if db_qualification:
            job.min_qualification = db_qualification.get()
            print("Already Exists")
        else:
            qualification.save()
            job.min_qualification = qualification
            print("Created New")

        job.save()

        role = experienceForm.cleaned_data[0]["role"]
        no_of_years = experienceForm.cleaned_data[0]["no_of_years"]

        experience_entries = Experience.objects.filter(
            role=role, no_of_years=no_of_years
        )

        if experience_entries:
            print(experience_entries)
            job.min_required_experience.add(experience_entries.get())
        else:
            new_experience = Experience(no_of_years=no_of_years, role=role)
            new_experience.save()
            job.min_required_experience.add(new_experience)

        jobForm.save_m2m()
        if skills_field:
            new_skill = Skill.objects.get_or_create(name=skills_field)
            job.required_skills.add(new_skill[0])
        job.save()
        return redirect("home")
    context = {
        "form": jobForm,
        "qualification": qualificationForm,
        "experience": experienceForm,
    }
    return render(request, "records/register.html", context)


@login_required(login_url="login")
@check_permission(profiletype="P")
def updateVacancy(request, id):
    vacancy = Vacancy.objects.get(pk=id)
    vacancyForm = VacancyRegistrationForm(
        request.POST or None, request.FILES or None, instance=vacancy
    )
    if vacancyForm.is_valid():
        vacancy = vacancyForm.save(commit=False)
        vacancy.save()
        vacancyForm.save_m2m()
        return redirect("home")
    context = {"form": vacancyForm}
    return render(request, "records/register.html", context)


# @login_required(login_url='login')
# @check_permission(profiletype='V')
def searchjobsview(request):
    context = {}

    if request.method == "POST":
        level = request.POST["Level"]
        skill = request.POST["Skill"]
        category = request.POST["Category"]
        if level:
            query_qualification_level = Qualification.objects.filter(level=level)
        else:
            query_qualification_level = Qualification.objects.all()
        print(query_qualification_level)
        jobs_filtered = []
        for item in query_qualification_level:
            qual_id = item.id
            job_querysets = Job.objects.filter(min_qualification_id=qual_id)
            if skill:
                job_querysets = job_querysets.filter(required_skills__in=[skill])
            if category:
                job_querysets = job_querysets.filter(category=category)
            if job_querysets.exists():
                print(job_querysets)
                jobs_filtered += job_querysets
        vacancy_filtered = Vacancy.objects.filter(
            job__in=jobs_filtered, deadline_date__gt=datetime.today()
        )
        print("Inside POST")
    else:
        jobs_filtered = Job.objects.all()
        vacancy_filtered = Vacancy.objects.filter(deadline_date__gt=datetime.today())
        print("Inside except")
    print(jobs_filtered)
    totalProvider = Provider.objects.all().count()
    totalApplicant = Applicant.objects.all().count()
    totalJob = Job.objects.all().count()
    context = {
        "form": JobSearchForm,
        "jobs": jobs_filtered,
        "total_jobs": totalJob,
        "total_companies": totalProvider,
        "total_candidates": totalApplicant,
        "vacancy_filtered": vacancy_filtered,
    }

    return render(request, "records/home.html", context)


def apply_for_job(request, vacancy_id):
    applicant = Applicant.objects.get(id=request.user.id)
    vacancy = Vacancy.objects.get(id=vacancy_id)
    vacancy.applications.add(applicant)
    return redirect("job_search")


def list_vacancy_details(request, vacancy_id):
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
        job = vacancy.job
        context = {"job": job, "vacancy": vacancy}
        print(job.min_required_experience.all())
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    except Vacancy.DoesNotExist:
        raise Http404("Vacancy does not exist")
    return render(request, "records/vacancy-detail-list.html", context)


def list_job_details(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        context = {"job": job}
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    return render(request, "records/job-detail-list.html", context)


def providerHome(request):
    try:
        provider = Provider.objects.get(id=request.user)
        jobs = Job.objects.filter(provider=provider)
        print(jobs)
        context = {"jobs": jobs}
        return render(request, "records/provider-home.html", context)
    except Provider.DoesNotExist:
        return redirect("provider_registration")


def home(request):
    if request.user.is_authenticated and request.user.profile_type == "P":
        return providerHome(request)
    return searchjobsview(request)


@login_required(login_url="login")
@check_permission(profiletype="P")
def deleteJob(request, job_id):
    job = Job.objects.get(id=job_id)
    job.delete()
    return redirect("home")


@login_required(login_url="login")
@check_permission(profiletype="P")
def deleteVacancy(request, vacancy_id):
    vacancy = Vacancy.objects.get(id=vacancy_id)
    vacancy.delete()
    return redirect("home")
