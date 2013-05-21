from django.contrib.gis.db import models

class Allotment(models.Model):
    name = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    geometry = models.MultiPolygonField(blank=True, null=True, geography=True)
    involved = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    acres = models.FloatField(blank=True, null=True)
    state = models.CharField(max_length=2)
    source = models.CharField(max_length=255)
    field_office = models.CharField(max_length=255, blank=True, null=True)
    
    objects = models.GeoManager()

    def simplified_geometry(self):
        return self.geometry.simplify(tolerance=0.001, preserve_topology=True).wkt

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
