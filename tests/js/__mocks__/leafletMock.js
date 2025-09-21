// tests/js/__mocks__/leafletMock.js
export function installLeafletMock() {
  const addTo = jest.fn().mockReturnThis();
  const on = jest.fn().mockReturnThis();
  const setView = jest.fn().mockReturnThis();

  global.L = {
    map: jest.fn(() => ({ setView, addLayer: jest.fn(), on: jest.fn() })),
    tileLayer: jest.fn(() => ({ addTo })),
    marker: jest.fn(() => ({ addTo })),
    polyline: jest.fn(() => ({ addTo })),
    layerGroup: jest.fn(() => ({ addTo })),
    icon: jest.fn(() => ({})),
    popup: jest.fn(() => ({
      setLatLng: jest.fn().mockReturnThis(),
      setContent: jest.fn().mockReturnThis(),
      openOn: jest.fn().mockReturnThis(),
    })),
    Icon: {
      Default: {
        mergeOptions: jest.fn(),
      },
    },
  };

  // GPX plugin mock (attach to L.GPX)
  const GpxMock = jest.fn().mockImplementation(() => ({
    on,
    addTo,
    getBounds: jest.fn(() => ({
      getCenter: jest.fn(() => [0, 0]),
    })),
    get_distance: jest.fn(() => 10000),
    get_elevation_gain: jest.fn(() => 500),
    get_total_time_string: jest.fn(() => '2h 30m'),
    get_start_marker: jest.fn(() => ({ setIcon: jest.fn() })),
    get_end_marker: jest.fn(() => ({
      setIcon: jest.fn(),
      _icon: { style: {}, setAttribute: jest.fn() },
    })),
    get_waypoint_markers: jest.fn(() => []),
  }));

  global.GPX = GpxMock;
  global.L.GPX = GpxMock;  // ✅ what maps.js actually checks
}



