// assets/js/maps.js
const apiKey = 'jOl45Inj6h9aQPbkE2LMEn0UlYs1aeTE';

// Build static URL for relative paths
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
      // Build explicit start/end icons so colors can’t be overridden
      const START_ICON = L.icon({
        iconUrl: window.GPX_MARKER_OPTS.startIconUrl,
        iconSize: [56, 56],
        iconAnchor: [28, 56],
        popupAnchor: [0, -52],
        className: 'accessible-marker'
      });
      const END_ICON = L.icon({
        iconUrl: window.GPX_MARKER_OPTS.endIconUrl,
        iconSize: [56, 56],
        iconAnchor: [28, 56],
        popupAnchor: [0, -52],
        className: 'accessible-marker'
      });

      const gpxLayer = new L.GPX(gpxUrl, {
        async: true,
        parseElements: ['track', 'route'], 
        marker_options: {
          ...window.GPX_MARKER_OPTS,
          startIcon: START_ICON,
          endIcon: END_ICON
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
      // if anything overrides icons, swap them back after load
      .on('loaded', () => window.applyAccessibleGpxIcons?.(gpxLayer))
      .on('loaded', () => {
        const end = gpxLayer.get_end_marker?.();
        if (end && end._icon) {
          end._icon.style.pointerEvents = 'none';
          end._icon.setAttribute('aria-hidden', 'true');
          end._icon.setAttribute('tabindex', '-1');
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
      // show a tiny help note below the map
      const note = document.createElement('div');
      note.className = 'route-info-box';
      note.innerHTML = `<small>Route overlay unavailable (GPX plugin not loaded).</small>`;
      el.parentNode.insertBefore(note, el.nextSibling);
    }
  });
}

// ---- Accessible Leaflet marker: global defaults + GPX support (red/green + 56px) ----
(function () {
  const makeMarkerSvg = (fill) => `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Map marker">
  <path d="M32 2c-12.15 0-22 9.85-22 22 0 16.5 22 38 22 38s22-21.5 22-38C54 11.85 44.15 2 32 2z"
        fill="${fill}" stroke="#083a8c" stroke-width="2"/>
  <circle cx="32" cy="24" r="10" fill="#ffffff"/>
</svg>`.trim();

  // If CSP blocks data:, switch to a static URL instead.
  const startSvgUrl = "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(makeMarkerSvg("#198754")); // green
  const endSvgUrl   = "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(makeMarkerSvg("#dc3545")); // red
  const wptSvgUrl   = "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(makeMarkerSvg("#0a58ca")); // blue (waypoints/plain)

  // 1) Plain Leaflet markers (fallbacks) use blue SVG and get a class for CSS sizing
  L.Icon.Default.mergeOptions({
    iconUrl: wptSvgUrl,
    iconRetinaUrl: wptSvgUrl,
    iconSize: [56, 56],
    iconAnchor: [28, 56],
    popupAnchor: [0, -52],
    className: "accessible-marker",
    shadowUrl: ""
  });

  // 2) GPX marker options (green start, red end, blue waypoints), also tagged with class
  window.GPX_MARKER_OPTS = {
    startIconUrl: startSvgUrl,
    endIconUrl: endSvgUrl,
    wptIconUrls: { "": wptSvgUrl },
    iconSize: [56, 56],
    iconAnchor: [28, 56],
    popupAnchor: [0, -52],
    className: "accessible-marker",
    shadowUrl: ""
  };

  // 3) If leaflet-gpx is present, set its defaults too
  if (L.GPX && L.GPX.prototype && L.GPX.prototype.options) {
    L.GPX.prototype.options.marker_options = Object.assign(
      {},
      L.GPX.prototype.options.marker_options,
      window.GPX_MARKER_OPTS
    );
  }

  // if a GPX layer was created before this ran, swap its icons post-load
  window.applyAccessibleGpxIcons = function (gpxLayer) {
    const mk = (url) => L.icon({
      iconUrl: url,
      iconSize: [56, 56],
      iconAnchor: [28, 56],
      popupAnchor: [0, -52],
      className: "accessible-marker"
    });
    gpxLayer.get_start_marker?.()?.setIcon(mk(startSvgUrl));
    gpxLayer.get_end_marker?.()?.setIcon(mk(endSvgUrl));
    (gpxLayer.get_waypoint_markers?.() || []).forEach(m => m.setIcon(mk(wptSvgUrl)));
  };
})();

// Run when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initRouteMaps, { once: true });
} else {
  initRouteMaps();
}

// Smooth scroll for View Route links that point to on-page anchors
document.querySelectorAll('a.scroll-link[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    const hash = link.getAttribute('href');      // e.g. "#route-snowdon-crib-goch"
    const target = document.querySelector(hash); // find the section by id

    if (!target) return; // no matching element; let the browser do its thing

    e.preventDefault();  // handle the scroll 
    const headerOffset = 60; // adjust for sticky header height
    const y = target.getBoundingClientRect().top + window.pageYOffset - headerOffset;

    window.scrollTo({ top: y, behavior: 'smooth' });
    history.replaceState(null, '', hash); // keep URL hash in sync

    // added for a11y: move focus to the section without jumping
    target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  });
});

// when landing on a URL with a hash, offset the initial jump
window.addEventListener('load', () => {
  if (location.hash) {
    const target = document.querySelector(location.hash);
    if (target) {
      const headerOffset = 60;
      const y = target.getBoundingClientRect().top + window.pageYOffset - headerOffset;
      window.scrollTo({ top: y, behavior: 'auto' });
    }
  }
});

