from rest_framework import serializers
from allotments.models import Allotment
import logging

class AllotmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allotment
        exclude = ('geometry',)

class GeoAllotmentSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField('simplified_geometry')

    class Meta:
        model = Allotment
        read_only_fields = ('geometry',)

    def simplified_geometry(self, obj):
        return obj.simplified_geometry()
