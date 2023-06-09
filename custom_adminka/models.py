from django.db import models


class CurrentUser(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} {self.first_name}"


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name
