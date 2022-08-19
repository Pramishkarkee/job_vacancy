from django.urls import path
from .views import (
    jobRegister,
    list_job_details,
    list_vacancy_details,
    vacancyRegister,
    updateJob,
    deleteJob,
    deleteVacancy,
    updateVacancy,
    searchjobsview,
    apply_for_job,
    home,
)

urlpatterns = [
    path("", home, name="home"),
    path("jobsearch/", searchjobsview, name="job_search"),
    path("jobregister/", jobRegister, name="job_register"),
    path("vacancyregister/<int:job_id>", vacancyRegister, name="vacancy_register"),
    path("jobupdate/<int:id>/", updateJob, name="job_update"),
    path("jobdelete/<int:job_id>/", deleteJob, name="job_delete"),
    path("vacancydelete/<int:vacancy_id>/", deleteVacancy, name="vacancy_delete"),
    path("vacancyupdate/<int:id>/", updateVacancy, name="vacancy_update"),
    path(
        "apply-for-job/<int:vacancy_id>/",
        apply_for_job,
        name="apply_for_job",
    ),
    path(
        "vacancy/<int:vacancy_id>/details/",
        list_vacancy_details,
        name="list_vacancy_details",
    ),
    path("job/<int:job_id>/details/", list_job_details, name="list_job_details"),
]
