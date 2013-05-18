//clustering activated = {{using_clustering}}
{% if using_clustering %}
var markers = new L.MarkerClusterGroup();
{% endif %}
$.get("{% url list_url_name %}", function(data){
	$.each(data, function(index, value){
		var marker = new L.Marker(new L.LatLng(value[2], value[1]));
		marker.on('mouseover', function(e) {
			marker.unbindPopup();
			$.get("{% url popup_url_name %}", { id : value[0] }, function (data){
				marker.bindPopup(data);
			});
		});
		{% if using_clustering %}
		markers.addLayer(marker);
		{% else %}
		marker.addTo(map);
		{% endif %}
	});
	{% if using_clustering %}
	map.addLayer(markers);
	{% endif %}
}, "json");