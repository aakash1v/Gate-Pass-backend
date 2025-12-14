from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Hostel(models.Model):
    HOSTEL_TYPE_CHOICES = [
        ("boys", "Boys"),
        ("girls", "Girls"),
    ]

    name = models.CharField(max_length=100, unique=True)
    hostel_type = models.CharField(max_length=10, choices=HOSTEL_TYPE_CHOICES)
    total_capacity = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    warden = models.ForeignKey(
        "users.WardenProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hostels"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.hostel_type})"
