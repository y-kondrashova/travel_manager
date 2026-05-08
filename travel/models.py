from django.db import models
from django.core.exceptions import ValidationError


class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def update_completion_status(self):
        places = self.places.all()

        if places.exists() and all(place.visited for place in places):
            self.completed = True
        else:
            self.completed = False
        self.save(update_fields=["completed"])

    def __str__(self):
        return self.name


class ProjectPlace(models.Model):
    project = models.ForeignKey(
        TravelProject, related_name="places", on_delete=models.CASCADE
    )

    external_id = models.IntegerField()
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True, default="")
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "external_id")

    def clean(self):
        if not self.pk and self.project.places.count() >= 10:
            raise ValidationError("Project cannot contain more than 10 places.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.update_completion_status()

    def __str__(self):
        return self.title
