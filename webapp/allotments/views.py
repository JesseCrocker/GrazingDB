from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from datetime import *
from django.conf import settings
import json
from django.core.serializers.json import DjangoJSONEncoder

from models import Allotment

def list(request):
    return render_to_response('allotmentList.html', 
        {} , context_instance=RequestContext(request))

def mapView(request):
    return render_to_response('map.html', 
        {} , context_instance=RequestContext(request))