// assets/js/maps.js
const apiKey = 'jOl45Inj6h9aQPbkE2LMEn0UlYs1aeTE';

// Build a static URL for relative paths
const STATIC_PREFIX = (window.STATIC_PREFIX || '/static/').replace(/\/+$/, '/');
const toStatic = (p) => {
  if (/^https?:\/\//i.test(p)) return p;          // absolute
  if (p.startsWith('/static/')) return p;          // already static
  return STATIC_PREFIX + p.replace(/^\/+/, '');    // make static-relative
};

function initRouteMaps() {
  if (typeof window.L === 'undefined') {
    console.error('[maps] Leaflet not loaded');
    return;
  }

  const maps = document.querySelectorAll('.route-map[id][data-gpx]');
  if (!maps.length) return;

  maps.forEach((el) => {
    const gpxAttr = el.getAttribute('data-gpx');
    const gpxUrl  = toStatic(gpxAttr);
    console.log('[maps] preparing map:', el.id, 'GPX:', gpxUrl);

    // 1) Always create the basemap
    const map = L.map(el.id).setView([54.5, -3.1], 12);

    L.tileLayer(
      `https://api.os.uk/maps/raster/v1/zxy/Outdoor_3857/{z}/{x}/{y}.png?key=${apiKey}`,
      { attribution: '© Crown copyright and database rights 2025 Ordnance Survey', maxZoom: 18 }
    ).addTo(map);

    // 2) Add GPX overlay if plugin is available
    if (typeof L.GPX === 'function') {
      const gpxLayer = new L.GPX(gpxUrl, {
        async: true,
        parseElements: ['track', 'route', 'waypoint'],
        marker_options: {
          startIconUrl: 'https://unpkg.com/leaflet-gpx@1.7.0/pin-icon-start.png',
          endIconUrl:   'https://unpkg.com/leaflet-gpx@1.7.0/pin-icon-end.png',
          shadowUrl:    'https://unpkg.com/leaflet-gpx@1.7.0/pin-shadow.png'
        },
        polyline_options: { color: '#007bff', weight: 4, opacity: 0.8, lineCap: 'round' }
      })
      .on('loaded', (e) => {
        const gpx = e.target;
        try {
          map.fitBounds(gpx.getBounds());

          const distanceKm = (gpx.get_distance?.() || 0) / 1000;
          const elevation  = gpx.get_elevation_gain?.() || 0;

          let time = typeof gpx.get_total_time_string === 'function' ? gpx.get_total_time_string() : '';
          if (!time) {
            const estimatedHours = distanceKm / 4 + elevation / 600;
            time = `~${estimatedHours.toFixed(1)} hrs est.`;
          }

          const stats = `
            <strong><i class="fas fa-route me-2"></i>Distance:</strong> ${distanceKm.toFixed(2)} km<br>
            <strong><i class="fas fa-mountain me-2"></i>Elevation gain:</strong> ${Math.round(elevation)} m<br>
            <strong><i class="far fa-clock me-2"></i>Time:</strong> ${time}
          `;

          L.popup()
            .setLatLng(gpx.getBounds().getCenter())
            .setContent(`<small>${stats}</small>`)
            .openOn(map);

          const infoBox = document.createElement('div');
          infoBox.className = 'route-info-box';
          infoBox.innerHTML = stats;
          el.parentNode.insertBefore(infoBox, el.nextSibling);

          console.log('[maps] GPX loaded OK:', gpxUrl,
            { distanceKm: distanceKm.toFixed(2), elevation: Math.round(elevation), time });
        } catch (err) {
          console.error('[maps] Error after GPX loaded:', gpxUrl, err);
        }
      })
      .on('addline', (e) => {
        // Helpful debug: polyline actually added
        console.log('[maps] polyline added for', gpxUrl, e.line.getLatLngs().length, 'points');
      })
      .on('error', (err) => {
        console.error('[maps] GPX load error:', gpxUrl, err);
      })
      .addTo(map);
    } else {
      console.warn('[maps] leaflet-gpx plugin not loaded; showing basemap without route:', gpxUrl);
      // Optional: show a tiny help note below the map
      const note = document.createElement('div');
      note.className = 'route-info-box';
      note.innerHTML = `<small>Route overlay unavailable (GPX plugin not loaded).</small>`;
      el.parentNode.insertBefore(note, el.nextSibling);
    }
  });
}

// Run when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initRouteMaps, { once: true });
} else {
  initRouteMaps();
}

// Smooth scroll for “View Route”
document.querySelectorAll('.scroll-link').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(link.dataset.target);
    if (target) window.scrollTo({ top: target.offsetTop - 60, behavior: 'smooth' });
  });
});



