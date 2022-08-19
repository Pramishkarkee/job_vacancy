from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self) -> str:
        return self.name

    @property
    def full_address(self) -> str:
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="province"
    )

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country"],
                name="Unique Province in a Country",
            )
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def full_address(self) -> str:
        return f"{self.name}, {self.country.full_address}"


class District(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, related_name="district"
    )

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "province"],
                name="Unique District in a Province",
            )
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def full_address(self) -> str:
        return f"{self.name}, {self.province.full_address}"


class VDCMunicipality(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="vdc_municipality"
    )

    class Meta:
        verbose_name = "VDC/Municipality"
        verbose_name_plural = "VDC/Municipalities"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "district"],
                name="Unique VDC/Municipality in a District",
            )
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def full_address(self) -> str:
        return f"{self.name}, {self.district.full_address}"


class WardNumber(models.Model):
    ward_number = models.IntegerField(blank=True, null=True, verbose_name="Ward Number")
    vdc_municipality = models.ForeignKey(
        VDCMunicipality,
        on_delete=models.CASCADE,
        related_name="ward_number",
        verbose_name="VDC/Municipality",
    )

    class Meta:
        verbose_name = "Ward Number"
        verbose_name_plural = "Ward Numbers"
        constraints = [
            models.UniqueConstraint(
                fields=["ward_number", "vdc_municipality"],
                name="Unique Ward Number in a VDC/Municipality",
            )
        ]

    def __str__(self) -> str:
        return f"{self.ward_number}"

    @property
    def full_address(self) -> str:
        vdc_municipality_name, district_name = self.vdc_municipality.full_address.split(
            ",", 1
        )
        return f"{vdc_municipality_name} - " f"{self.ward_number}, {district_name}"
