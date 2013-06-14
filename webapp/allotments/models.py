from django.contrib.gis.db import models
import logging

class Allotment(models.Model):
    name = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    geometry = models.MultiPolygonField(blank=True, null=True)
    involved = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    acres = models.FloatField(blank=True, null=True)
    state = models.CharField(max_length=2)
    source = models.CharField(max_length=255)
    field_office = models.CharField(max_length=255, blank=True, null=True)
    
    objects = models.GeoManager()

    def simplified_geometry(self):
        return self.geometry.simplify(tolerance=0.001, preserve_topology=True).wkt

    def lookup_district(self):
        try:
            simplifed_geom = self.geometry.simplify(tolerance=0.001, preserve_topology=True)
            districts = District.objects.filter(agency=self.agency, geometry__intersects=simplifed_geom).all()[:1]
            if len(districts):
                district = districts[0]
                return district.name
            else:
                logging.debug('no distircts found')
        except Exception, e:
            logging.debug(e)

        return None

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


class District(models.Model):
    name = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    parent_unit = models.CharField(max_length=255,blank=True, null=True)
    state = models.CharField(max_length=2)
    geometry = models.MultiPolygonField(blank=True, null=True, geography=True)
    source = models.CharField(max_length=255)

    objects = models.GeoManager()

    def simplified_geometry(self):
        return self.geometry.simplify(tolerance=0.001, preserve_topology=True).wkt
