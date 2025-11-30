// CampusMap with Collapsible Narrow Sidebar
// Location: src/components/Map/CampusMap.jsx

import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, Tooltip } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { buildingsAPI, navigationAPI } from '../../services/api';
import { showToast } from '../../utils/helpers';
import './CampusMap.css';

// Fix Leaflet default marker icons
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

function CampusMap() {
  const [buildings, setBuildings] = useState([]);
  const [selectedStart, setSelectedStart] = useState('');
  const [selectedEnd, setSelectedEnd] = useState('');
  const [routeData, setRouteData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const mapCenter = [12.963718, 77.506037];
  const mapZoom = 16;

  useEffect(() => {
    fetchBuildings();
  }, []);

  const fetchBuildings = async () => {
    try {
      const response = await buildingsAPI.getAll();
      setBuildings(response.data.buildings || []);
    } catch (error) {
      console.error('Error fetching buildings:', error);
      showToast('Failed to load buildings', 'error');
    }
  };

  const handleFindRoute = async () => {
    if (!selectedStart || !selectedEnd || selectedStart === '' || selectedEnd === '') {
      showToast('Please select both start and end buildings', 'warning');
      return;
    }

    if (selectedStart === selectedEnd) {
      showToast('Start and end buildings cannot be the same', 'warning');
      return;
    }

    setLoading(true);
    setRouteData(null);

    try {
      const response = await navigationAPI.calculateRoute(
        parseInt(selectedStart),
        parseInt(selectedEnd)
      );

      setRouteData(response.data);
      showToast('Route calculated successfully!', 'success');
    } catch (error) {
      console.error('Error calculating route:', error);
      const errorMsg = error.response?.data?.error || 'Failed to calculate route';
      showToast(errorMsg, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleClearRoute = () => {
    setSelectedStart('');
    setSelectedEnd('');
    setRouteData(null);
  };

  const getRouteCoordinates = () => {
    if (!routeData || !routeData.route) return [];
    return routeData.route.map(point => [point.lat, point.lng]);
  };

  const getStartBuilding = () => {
    if (!selectedStart || selectedStart === '') return null;
    return buildings.find(b => b.building_id === parseInt(selectedStart));
  };

  const getEndBuilding = () => {
    if (!selectedEnd || selectedEnd === '') return null;
    return buildings.find(b => b.building_id === parseInt(selectedEnd));
  };

  const createIcon = (color) => {
    return new L.Icon({
      iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
      shadowUrl: markerShadow,
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
  };

  const buildingIcon = createIcon('blue');
  const startIcon = createIcon('green');
  const endIcon = createIcon('red');
  const waypointIcon = createIcon('violet');

  return (
    <div className="campus-map-container">
      {/* Collapsible Sidebar */}
      <div className={`map-sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <button 
          className="collapse-btn"
          onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {sidebarCollapsed ? '▶' : '◀'}
        </button>

        {!sidebarCollapsed && (
          <div className="sidebar-content">
            <h2>🗺️ Navigation</h2>

            {/* Route Selector */}
            <div className="route-selector">
              <div className="form-group">
                <label htmlFor="start">🟢 Start</label>
                <select
                  id="start"
                  value={selectedStart}
                  onChange={(e) => {
                    setSelectedStart(e.target.value);
                    setRouteData(null);
                  }}
                >
                  <option value="">Select...</option>
                  {buildings.map(building => (
                    <option key={building.building_id} value={building.building_id}>
                      {building.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="end">🔴 End</label>
                <select
                  id="end"
                  value={selectedEnd}
                  onChange={(e) => {
                    setSelectedEnd(e.target.value);
                    setRouteData(null);
                  }}
                >
                  <option value="">Select...</option>
                  {buildings.map(building => (
                    <option key={building.building_id} value={building.building_id}>
                      {building.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="button-group">
                <button
                  onClick={handleFindRoute}
                  disabled={!selectedStart || !selectedEnd || loading}
                  className="btn btn-primary"
                >
                  {loading ? '⏳' : '🧭'} Route
                </button>
                <button
                  onClick={handleClearRoute}
                  className="btn btn-secondary"
                  disabled={!selectedStart && !selectedEnd}
                >
                  Clear
                </button>
              </div>
            </div>

            {/* Selected Buildings */}
            {(getStartBuilding() || getEndBuilding()) && (
              <div className="selected-buildings">
                {getStartBuilding() && (
                  <div className="building-info">
                    <span className="dot green"></span>
                    <span className="text">Start: {getStartBuilding().name}</span>
                  </div>
                )}
                {getEndBuilding() && (
                  <div className="building-info">
                    <span className="dot red"></span>
                    <span className="text">End: {getEndBuilding().name}</span>
                  </div>
                )}
              </div>
            )}

            {/* Route Information */}
            {routeData && (
              <div className="route-info">
                <h3>📍 Route Details</h3>

                {/* Stats - Stacked vertically for narrow sidebar */}
                <div className="route-stats">
                  <div className="stat">
                    <span className="stat-icon">📏</span>
                    <div className="stat-content">
                      <span className="stat-label">Distance</span>
                      <span className="stat-value">{routeData.total_distance}m</span>
                    </div>
                  </div>
                  <div className="stat">
                    <span className="stat-icon">⏱️</span>
                    <div className="stat-content">
                      <span className="stat-label">Time</span>
                      <span className="stat-value">{routeData.estimated_time_minutes} min</span>
                    </div>
                  </div>
                  <div className="stat">
                    <span className="stat-icon">🔀</span>
                    <div className="stat-content">
                      <span className="stat-label">Waypoints</span>
                      <span className="stat-value">{routeData.waypoints_count}</span>
                    </div>
                  </div>
                </div>

                {/* Directions */}
                {routeData.directions && routeData.directions.length > 0 && (
                  <div className="directions">
                    <h4>🚶 Directions</h4>
                    <div className="directions-list">
                      {routeData.directions.map((direction) => (
                        <div key={direction.step} className="direction-item">
                          <span className="step-number">{direction.step}</span>
                          <div className="direction-content">
                            <span className="direction-text">{direction.instruction}</span>
                            {direction.distance > 0 && (
                              <span className="direction-distance">({direction.distance}m)</span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Map Container */}
      <div className="map-wrapper">
        <MapContainer
          center={mapCenter}
          zoom={mapZoom}
          style={{ height: '100%', width: '100%' }}
          zoomControl={true}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {buildings.map(building => {
            const isStart = selectedStart && selectedStart !== '' && building.building_id === parseInt(selectedStart);
            const isEnd = selectedEnd && selectedEnd !== '' && building.building_id === parseInt(selectedEnd);

            let icon = buildingIcon;
            if (isStart) icon = startIcon;
            if (isEnd) icon = endIcon;

            return (
              <Marker
                key={building.building_id}
                position={[building.latitude, building.longitude]}
                icon={icon}
              >
                <Popup>
                  <div className="building-popup">
                    <h3>{building.name}</h3>
                    <p><strong>Code:</strong> {building.code}</p>
                    {building.description && <p>{building.description}</p>}
                  </div>
                </Popup>
              </Marker>
            );
          })}

          {routeData && routeData.route && routeData.route.length > 0 && (
            <Polyline
              positions={getRouteCoordinates()}
              color="#667eea"
              weight={5}
              opacity={0.8}
              smoothFactor={1}
            />
          )}

          {routeData && routeData.route && routeData.route.map((point, index) => {
            if (point.type === 'waypoint') {
              return (
                <Marker
                  key={`waypoint-${index}`}
                  position={[point.lat, point.lng]}
                  icon={waypointIcon}
                >
                  <Tooltip permanent={false} direction="top">
                    <div className="waypoint-tooltip">
                      <strong>{point.name}</strong>
                      <div>Step {point.sequence}</div>
                    </div>
                  </Tooltip>
                </Marker>
              );
            }
            return null;
          })}
        </MapContainer>
      </div>
    </div>
  );
}

export default CampusMap;
