from django.contrib.gis.db import models

class Allotment(models.Model):
    name = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    geometry = models.MultiPolygonField(blank=True, null=True, geography=True)
    involved = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    acres = models.FloatField(blank=True, null=True)
    state = models.CharField(max_length=2)

    objects = models.GeoManager()

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "agency": self.agency,
            "geometry": self.geometry.wkt,
            "involved": self.involved,
            "notes": self.notes,
            "acres": self.acres,
        }