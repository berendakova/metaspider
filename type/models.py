from django.db import models


# Create your models here.

class Type(models.Model):
    name = models.CharField(db_index=True, max_length=255, unique=False)
