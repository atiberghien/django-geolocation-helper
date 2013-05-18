from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos.point import Point

from geopy import geocoders

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
    
    class Meta:
        abstract = True

def update_geolocation(sender, instance, **kwargs):
    """
    This signal receiver update the instance but does not save it
    Should be used with pre_save signal
    """
    g = geocoders.GoogleV3()
    try:
        place, (lat, lng) = g.geocode(instance.get_location_as_string())
        instance.geom = Point(lng, lat)
    except:
        instance.geom = None