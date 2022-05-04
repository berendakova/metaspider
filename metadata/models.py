from django.db import models


class MetadataManager(models.Manager):
    def create_metadata(self, response):
        metadata = self.model()
        metadata.response = response

        metadata.save()

        return metadata


class Metadata(models.Model):
    response = models.JSONField(db_index=True, unique=True)
    objects = MetadataManager()


