ymaps.ready(init);
function init() {
    let locationInput = document.getElementById('remember_location');
    locationInput.disabled = true;
    let ymap = new ymaps.Map("YMapsID", {
        center: [55.76, 37.64],
        zoom: 6,
        controls: ['typeSelector', 'fullscreenControl', 'zoomControl']
    });
    ymap.events.add('click', function (e) {
        var currentPoint = e.get('coords');
        ymap.geoObjects.removeAll();
        ymap.geoObjects.add(new ymaps.Placemark(currentPoint));
        ymaps.geocode(currentPoint).then(function (res) {
            let geoObject = res.geoObjects.get(0);
            locationInput.value = geoObject.getAddressLine();
        });
    });
    document.getElementById('submit_remember_form').addEventListener("click", function() {
        document.getElementById('remember_location').disabled = false;
    });
}