from rest_framework import serializers
from allotments.models import Allotment
import logging

class AllotmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allotment
        exclude = ('geometry',)

class GeoAllotmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allotment
