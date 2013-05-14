from distutils.core import setup

setup(
    name='django-geolocation-helper',
    version = '0.x',
    
    author = 'Alban Tiberghien (@tiberghien)',
    description = 'Helper for geolocated model (based on leaflet)',
    license = 'GNU GPL',
    
    packages = ['geolocation_helper', 'geolocation_helper/templatetags']
)