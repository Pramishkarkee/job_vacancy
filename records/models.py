import uuid
from datetime import date

from address.models import WardNumber
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from professional.models import Category, Experience, Qualification, Skill

from records.choices import (
    EMPLOYMENT_STATUS_CHOICES,
    GENDER_CHOICES,
    PROFILE_TYPE_CHOICES,
)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    middle_name = models.CharField(
        max_length=150, blank=True, null=False, verbose_name="Middle Name"
    )

    contact_number = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="Contact Number"
    )

    profile_photo = models.ImageField(
        verbose_name="Profile Picture",
        upload_to="users/profile-photo/",
        null=False,
        blank=False,
        default="users/default.jpg",
    )

    profile_type = models.CharField(
        max_length=1, choices=PROFILE_TYPE_CHOICES, blank=False, null=False
    )

    is_registered = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        "first_name",
        "email",
        "contact_number",
    ]

    def get_full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.get_full_name()

    def save(self, *args, **kwargs) -> None:
        if self.profile_type == "P":
            self.last_name = ""
        super(User, self).save(*args, **kwargs)


class Admin(User):
    def save(self, *args, **kwargs) -> None:
        self.set_password(self.password)
        self.is_superuser = True
        self.is_staff = True
        self.profile_type = "S"
        super(Admin, self).save(*args, **kwargs)


class Applicant(models.Model):
    id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        to_field="id",
        primary_key=True,
        related_name="applicant",
        verbose_name="ID",
        limit_choices_to={"profile_type": "A"},
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Gender",
        blank=False,
        null=False,
    )

    temporary_address = models.ForeignKey(
        WardNumber,
        on_delete=models.RESTRICT,
        related_name="applicant_temporary",
        verbose_name="Temporary Address",
    )

    permanent_address = models.ForeignKey(
        WardNumber,
        on_delete=models.RESTRICT,
        related_name="applicant_permanent",
        verbose_name="Permanent Address",
    )

    date_of_birth = models.DateField(
        verbose_name="Date of Birth",
        auto_now_add=False,
        blank=False,
        null=False,
    )

    qualification = models.ForeignKey(
        Qualification, on_delete=models.RESTRICT, related_name="applicant"
    )

    skills = models.ManyToManyField(Skill, related_name="applicant", blank=False)

    experience = models.ManyToManyField(
        Experience, related_name="applicant", blank=False
    )

    cv = models.FileField(
        verbose_name="CV", upload_to="users/cv", null=False, blank=False
    )

    supporting_document = models.FileField(
        verbose_name="Supporting Document",
        upload_to="users/supporting",
        blank=True,
        null=True,
        help_text="Combine all your supporting documents"
        + "into a single PDF file before uploading.",
    )

    profile_links = ArrayField(
        models.URLField(max_length=200),
        null=True,
        blank=True,
        verbose_name="Links to Professional Profiles",
    )

    interested_categories = models.ManyToManyField(
        Category, related_name="applicant_interested"
    )

    employment_status = models.CharField(
        max_length=50, choices=EMPLOYMENT_STATUS_CHOICES, blank=False, null=False
    )

    @property
    def full_name(self) -> str:
        return self.id.get_full_name()

    @property
    def age(self) -> int:
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    def __str__(self) -> str:
        return self.full_name

    def save(self, *args, **kwargs) -> None:
        self.id.save(*args, **kwargs)
        super(Applicant, self).save(*args, **kwargs)


class Provider(models.Model):
    id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        to_field="id",
        primary_key=True,
        related_name="provider",
        verbose_name="ID",
        limit_choices_to={"profile_type": "P"},
    )

    address = models.ForeignKey(
        WardNumber,
        on_delete=models.RESTRICT,
        related_name="provider",
        verbose_name="Address",
    )

    website = models.URLField(max_length=255, blank=True, null=False)

    categories_covered = models.ManyToManyField(
        Category, related_name="provider", blank=False
    )

    description = models.CharField(max_length=500, blank=False, null=False)

    def __str__(self) -> str:
        return self.id.__str__()

    def save(self, *args, **kwargs) -> None:
        self.id.save(*args, **kwargs)
        super(Provider, self).save(*args, **kwargs)
