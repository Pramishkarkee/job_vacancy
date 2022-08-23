from records.decorators import check_permission
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from records.models import Applicant
from .forms import QualificationSearchForm
from .models import Qualification


@login_required(login_url="login")
@check_permission(profiletype="P")
def search_view(request):
    context = {}

    if request.method == "POST":
        level = request.POST["level"]
        skill = request.POST["Skill"]
        category = request.POST["Category"]
        if level:
            query_qualification_level = Qualification.objects.filter(level=level)
        else:
            query_qualification_level = Qualification.objects.all()


        applicants = []
        for item in query_qualification_level:
            qual_id = item.id
            applicant_querysets = Applicant.objects.filter(qualification_id=qual_id)
            if skill:
                applicant_querysets = applicant_querysets.filter(skills__in=[skill])
            if category:
                applicant_querysets = applicant_querysets.filter(
                    interested_categories__in=[category]
                )
            if applicant_querysets.exists():
                applicants += applicant_querysets

    else:
        applicants = Applicant.objects.all()
    searchform = QualificationSearchForm()
    context = {"form": searchform, "applicants": applicants}

    return render(request, "records/search.html", context)
