from django.db import models


class Students(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True)
    year = models.IntegerField()
    verified = models.BooleanField(null=True, default=False)
    field_of_study = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"