from django.db import models
from django.contrib import admin
from django.forms.widgets import CheckboxSelectMultiple

from jobs.models import Job, Vacancy


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
