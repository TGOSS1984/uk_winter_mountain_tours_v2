const apiKey = 'jOl45Inj6h9aQPbkE2LMEn0UlYs1aeTE';

    function loadMap(mapId, gpxPath, lat, lon, zoom = 13) {
      const map = L.map(mapId).setView([lat, lon], zoom);

      L.tileLayer(`https://api.os.uk/maps/raster/v1/zxy/Outdoor_3857/{z}/{x}/{y}.png?key=${apiKey}`, {
        attribution: '© Crown copyright and database rights 2025 Ordnance Survey',
        maxZoom: 18
      }).addTo(map);

      new L.GPX(gpxPath, {
        async: true,
        marker_options: {
          startIconUrl: 'https://unpkg.com/leaflet-gpx@1.7.0/pin-icon-start.png',
          endIconUrl: 'https://unpkg.com/leaflet-gpx@1.7.0/pin-icon-end.png',
          shadowUrl: 'https://unpkg.com/leaflet-gpx@1.7.0/pin-shadow.png'
        },
        polyline_options: {
          color: '#007bff',
          weight: 4,
          opacity: 0.8,
          lineCap: 'round'
        }
      }).on('loaded', function(e) {
        const gpx = e.target;
        map.fitBounds(gpx.getBounds());

        const distanceKm = gpx.get_distance() / 1000;
        const elevation = gpx.get_elevation_gain();

        let time;
        if (typeof gpx.get_total_time_string === 'function') {
          time = gpx.get_total_time_string();
        }
        if (!time) {
          const estimatedHours = (distanceKm / 4) + (elevation / 600);
          time = `~${estimatedHours.toFixed(1)} hrs est.`;
        }

        const stats = `
            <strong><i class="fas fa-route me-2"></i>Distance:</strong> ${distanceKm.toFixed(2)} km<br>
            <strong><i class="fas fa-mountain me-2"></i>Elevation gain:</strong> ${Math.round(elevation)} m<br>
            <strong><i class="far fa-clock me-2"></i>Time:</strong> ${time}
            `;

        // Show Leaflet popup
        L.popup()
          .setLatLng(gpx.getBounds().getCenter())
          .setContent(`<small>${stats}</small>`)
          .openOn(map);

        // Show info box below map
        const mapElement = document.getElementById(mapId);
        if (mapElement) {
          const infoBox = document.createElement('div');
          infoBox.className = 'route-info-box';
          infoBox.innerHTML = stats;
          mapElement.parentNode.insertBefore(infoBox, mapElement.nextSibling);
        } else {
          console.warn(`Map element not found for ID: ${mapId}`);
        }
      }).addTo(map);
    }

    loadMap('map-helvellyn', 'routes/lake-district/helvellyn-striding-swirral.gpx', 54.5272, -3.0165);
    loadMap('map-blencathra-halls', 'routes/lake-district/blencathra-halls-fell.gpx', 54.6411, -3.0810);
    loadMap('map-blencathra-sharp', 'routes/lake-district/blencathra-sharp-edge.gpx', 54.6411, -3.0487);
    loadMap('map-pavey', 'routes/lake-district/pavey-ark-jacks-rake.gpx', 54.4551, -3.1050);
    loadMap('map-scafell', 'routes/lake-district/scafell-pike-lords-rake.gpx', 54.4543, -3.2115);
    loadMap('map-bowfell', 'routes/lake-district/bowfell-climbers-traverse.gpx', 54.4480, -3.1475);
    loadMap('map-gable', 'routes/lake-district/great-gable.gpx', 54.4889, -3.2284);
    loadMap('map-pillar', 'routes/lake-district/pillar.gpx', 54.5065, -3.2735);
    loadMap('map-fairfield', 'routes/lake-district/fairfield-horseshoe.gpx', 54.4484, -2.9623);
    loadMap('map-crinkle', 'routes/lake-district/crinkle-crags.gpx', 54.4378, -3.1473);

    document.querySelectorAll('.scroll-link').forEach(link => {
      link.addEventListener('click', e => {
        e.preventDefault();
        const target = document.querySelector(link.dataset.target);
        if (target) {
          window.scrollTo({ top: target.offsetTop - 60, behavior: 'smooth' });
        }
      });
    });