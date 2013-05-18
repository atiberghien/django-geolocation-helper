from django.views.generic.base import View
from django.http.response import HttpResponse
from django.template.loader import render_to_string

from .models import GeoLocatedModel

import json

class GeoLocatedModelJsonList(View): 
    model = None
    
    def get_queryset(self):
        if issubclass(self.model, GeoLocatedModel):
            return self.model.objects.filter(geom__isnull=False)
        else:
            raise NotImplementedError
    
    def prepare_queryset_to_json(self):
        raise NotImplementedError
    
    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps(self.prepare_queryset_to_json()),
                            mimetype='application/json')
        
class GeolocatedModelMarkerPopup(View):  
    model = None
    template_name = None
    template_var_name = None
    
    def get(self, request, *args, **kwargs):
        
        obj = self.model.objects.get(id=request.GET.get("id"))
        
        popup = render_to_string(self.template_name, 
                                {self.template_var_name : obj})
        
        return HttpResponse(popup,
                            mimetype='application/html')