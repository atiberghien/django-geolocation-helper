from django import template

register = template.Library()

@register.inclusion_tag('geolocation_helper/leaflet_fetch_geolocated.js')
def load_markers(list_url_name, popup_url_name, using_clustering=True):
    return {'list_url_name' : list_url_name,
            'popup_url_name' : popup_url_name,
            'using_clustering' : using_clustering}
    