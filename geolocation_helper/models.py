from django.conf import settings
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos.point import Point

import json
import urllib2

class GeoLocatedModel(geomodels.Model):
    geom = geomodels.PointField(null=True, blank=True)
    
    objects = geomodels.GeoManager()
    
    def get_location_as_string(self):
        """
        Should return a string for the address as Google Maps format
        """
        raise NotImplementedError
    
    def is_geolocated(self):
        """
        Usefull for example in the admin in order to easily identify non geolocated object
        """
        return self.geom is not None
    is_geolocated.boolean = True
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        def request_mapquest(location):
            mapquest_params = [
                "key=%s" % settings.MAPQUEST_APIKEY,
                'inFormat=kvp',
                'outFormat=json',
                'thumbMaps=false',
                'maxResults=1',
                'location=%s' % location
            ]
            mapquest_url = "http://open.mapquestapi.com/geocoding/v1/address?%s" % "&".join(mapquest_params)
            response = urllib2.urlopen(mapquest_url)
            data = json.load(response)
            return data["results"][0]["locations"][0]["latLng"]
        
        
           
        try:
            latlng = request_mapquest(urllib2.quote(self.get_location_as_string().encode('utf8')))
            self.geom = Point(latlng["lng"], latlng["lat"])
        except Exception, e:
            try:
                latlng = request_mapquest(urllib2.quote(self.city.encode('utf8')))
                self.geom = Point(latlng["lng"], latlng["lat"])
            except Exception, e:
                print self.id, self.get_location_as_string()
                print 10*"-"
        
        return geomodels.Model.save(self, 
                                    force_insert=force_insert, 
                                    force_update=force_update, 
                                    using=using, 
                                    update_fields=update_fields)
    
    class Meta:
        abstract = True