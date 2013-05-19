from allotments.models import Allotment
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from serializers import AllotmentSerializer, GeoAllotmentSerializer
from django.views.decorators.csrf import csrf_exempt 

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'allotments': reverse('allotment-list', request=request),
    })


class AllotmentList(generics.ListAPIView):
    """
    API endpoint that represents a list of allotments.
    """
    model = Allotment
    serializer_class = AllotmentSerializer


class AllotmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single allotment.
    """
    permission_classes = (permissions.IsAuthenticated,)
    model = Allotment
    serializer_class = AllotmentSerializer


class GeoAllotmentList(generics.ListAPIView):
    """
    API endpoint that represents a list of allotments, with geometry
    """
    permission_classes = (permissions.IsAuthenticated,)
    model = Allotment
    serializer_class = GeoAllotmentSerializer


class GeoAllotmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single allotment, with geometry
    """
    permission_classes = (permissions.IsAuthenticated,)
    model = Allotment
    serializer_class = GeoAllotmentSerializer
