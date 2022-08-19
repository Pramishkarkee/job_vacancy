from django.db import models

from professional.choices import QUALIFICATION_LEVEL_CHOICES


class Qualification(models.Model):
    level = models.CharField(
        max_length=10,
        choices=QUALIFICATION_LEVEL_CHOICES,
        verbose_name="Qualification Level",
        blank=False,
        null=False,
    )

    field = models.CharField(
        max_length=100,
        verbose_name="Qualification Field",
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return f"{self.level} in {self.field}"


class Category(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    desription = models.CharField(
        max_length=500, verbose_name="Description", blank=True, null=False
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Skill(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Name of the skill",
        blank=False,
        null=False,
        unique=True,
    )

    description = models.CharField(
        max_length=750, verbose_name="Description", blank=True, null=False
    )

    def __str__(self) -> str:
        return self.name


class Experience(models.Model):
    role = models.CharField(max_length=100, blank=False, null=False)
    no_of_years = models.IntegerField(blank=False, null=False)

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        constraints = [
            models.UniqueConstraint(
                fields=["role", "no_of_years"],
                name="One entry for a number of year for a role",
            )
        ]

    def __str__(self) -> str:
        return f"{self.no_of_years} years as {self.role}"
