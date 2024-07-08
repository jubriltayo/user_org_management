from django.db import models
from users.models import User



class Organisation(models.Model):
    orgId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name="organisations")

    def __str__(self):
        return self.name
    