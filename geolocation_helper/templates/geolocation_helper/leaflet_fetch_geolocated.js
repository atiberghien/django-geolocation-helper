//clustering activated = {{using_clustering}}

var layers = {
{% for layer in layers %}
"{{layer.id}}" : new L.{% if using_clustering %}MarkerClusterGroup{% else %}LayerGroup{% endif %}(),
{% empty %}
"-1" : new L.{% if using_clustering %}MarkerClusterGroup{% else %}LayerGroup{% endif %}(),
{% endfor %}
};

$.each(layers, function(index, value){
	var markers = value;
	var list_url_name = "{% url list_url_name %}";
	if(index != "-1"){
		list_url_name += "?layer_id=" + index
	}
	$.get(list_url_name, function(data){
		$.each(data, function(index, value){
			var marker = new L.Marker(new L.LatLng(value[2], value[1]));
			marker.on('mouseover', function(e) {
				marker.unbindPopup();
				$.get("{% url popup_url_name %}", { id : value[0] }, function (data){
					marker.bindPopup(data);
				});
			});
			markers.addLayer(marker);
		});
		map.addLayer(markers);
	}, "json");
});