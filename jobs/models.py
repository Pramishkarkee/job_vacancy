from datetime import datetime

from django.db import models

from records.models import Applicant, Provider
from professional.models import Experience, Category, Qualification, Skill


class Job(models.Model):
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, blank=False, null=False, related_name="job"
    )

    name = models.CharField(max_length=150, blank=False, null=False)

    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        related_name="job",
        blank=False,
        null=False,
    )

    position = models.CharField(max_length=200, blank=False, null=False)

    min_qualification = models.ForeignKey(
        Qualification,
        on_delete=models.RESTRICT,
        blank=False,
        null=False,
        verbose_name="Minimum Required Qualification",
    )

    min_required_experience = models.ManyToManyField(
        Experience, related_name="job", verbose_name="Minimum Required Experience"
    )

    required_skills = models.ManyToManyField(Skill, related_name="job", blank=False)

    description = models.CharField(max_length=500, null=False, blank=False)

    allowance = models.IntegerField(
        null=True, blank=True, verbose_name="Allowance (if any)"
    )

    def __str__(self) -> str:
        return self.name


class Vacancy(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="vacancy")

    is_part_time = models.BooleanField(
        default=False, blank=False, null=False, verbose_name="Part Time"
    )

    num_vacancies = models.IntegerField(
        null=False, blank=False, verbose_name="Number of vacancies"
    )

    notice_image = models.FileField(
        upload_to="jobs/notice-images",
        null=False,
        blank=False,
        verbose_name="Announcement Notice",
    )

    announced_date = models.DateTimeField(default=datetime.now, blank=False, null=False)

    deadline_date = models.DateTimeField(
        auto_now_add=False,
        verbose_name="Last Application Date",
        blank=False,
        null=False,
    )

    applications = models.ManyToManyField(Applicant, related_name="vacancy", blank=True)

    def __str__(self) -> str:
        return self.job.__str__()

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"
