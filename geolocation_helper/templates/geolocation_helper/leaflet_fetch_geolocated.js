var markers = new L.MarkerClusterGroup();
$.get("{% url list_url_name %}", function(data){
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