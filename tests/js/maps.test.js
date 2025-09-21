/** @jest-environment jsdom */
import { installLeafletMock } from './__mocks__/leafletMock';

function loadMapsJS() {
  jest.resetModules();
  installLeafletMock();

  // ✅ Must match selector in maps.js: .route-map[id][data-gpx]
  document.body.innerHTML = `
    <div id="map" class="route-map" data-gpx="/static/routes/test.gpx" style="height:400px"></div>
  `;

  Object.defineProperty(document, 'readyState', { value: 'complete', configurable: true });

  // import your file AFTER mocks/DOM exist
  require('../../assets/js/maps.js');
}

describe('maps.js', () => {
  beforeEach(() => {
    document.body.innerHTML = '';
    delete window.__mtv2_init_maps; // if guard like script.js
  });

  test('initialises a Leaflet map and base layer', () => {
    loadMapsJS();
    expect(L.map).toHaveBeenCalled();
    expect(L.tileLayer).toHaveBeenCalled();
  });

  test('adds a GPX layer when a GPX URL is provided', () => {
    loadMapsJS();
    expect(GPX).toHaveBeenCalled();
    const args = GPX.mock.calls[0];
    expect(args[1]).toEqual(expect.objectContaining({ async: true })); 
  });

  test('defensive: no crash if #map missing', () => {
    jest.resetModules();
    installLeafletMock();
    // no .route-map element present
    document.body.innerHTML = '<div id="not-map"></div>';
    expect(() => require('../../assets/js/maps.js')).not.toThrow();
  });
});