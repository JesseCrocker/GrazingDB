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
        'allotments with geometry': reverse('allotment-geo-list', request=request),
        'allotment detail': reverse('allotment-detail', args=[1], request=request),
        'allotment detail with geometry': reverse('allotment-detail', args=[1], request=request),
    })


class AllotmentList(generics.ListAPIView):
    """
    API endpoint that represents a list of allotments.
    """
    model = Allotment
    serializer_class = AllotmentSerializer

    def get_queryset(self):
        state = self.request.GET.get('state', None)
        if state:
            return Allotment.objects.filter(state=state)
        else:
            return Allotment.objects.all()


class AllotmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single allotment.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    model = Allotment
    serializer_class = AllotmentSerializer


class GeoAllotmentList(generics.ListAPIView):
    """
    API endpoint that represents a list of allotments, with geometry
    """
    model = Allotment
    serializer_class = GeoAllotmentSerializer

    def get_queryset(self):
        state = self.request.GET.get('state', None)
        if state:
            return Allotment.objects.filter(state=state)
        else:
            return Allotment.objects.all()


class GeoAllotmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single allotment, with geometry
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    model = Allotment
    serializer_class = GeoAllotmentSerializer
