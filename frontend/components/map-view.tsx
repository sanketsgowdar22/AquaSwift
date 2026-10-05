"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline, Polygon, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

/* Fix Leaflet default marker icons in Next.js */
const DefaultIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const DriverIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
  className: "hue-rotate-[200deg] saturate-150",
});

L.Marker.prototype.options.icon = DefaultIcon;

export interface MarkerData {
  position: [number, number];
  label?: string;
  type?: "customer" | "driver" | "default";
}

interface MapViewProps {
  center?: [number, number];
  zoom?: number;
  markers?: MarkerData[];
  route?: [number, number][];
  polygon?: [number, number][];
  polygons?: { id: string; coords: [number, number][]; color?: string; label?: string }[];
  height?: string;
  className?: string;
  onMapClick?: (latlng: { lat: number; lng: number }) => void;
  interactive?: boolean;
}

/* Sub-component to handle map click events */
function MapClickHandler({ onClick }: { onClick?: (latlng: { lat: number; lng: number }) => void }) {
  const map = useMap();
  useEffect(() => {
    if (!onClick) return;
    const handler = (e: L.LeafletMouseEvent) => onClick(e.latlng);
    map.on("click", handler);
    return () => { map.off("click", handler); };
  }, [map, onClick]);
  return null;
}

/* Default center: Banavasi/Hyderabad region */
const DEFAULT_CENTER: [number, number] = [15.3647, 75.1240];

export default function MapView({
  center = DEFAULT_CENTER,
  zoom = 14,
  markers = [],
  route,
  polygon,
  polygons,
  height = "300px",
  className = "",
  onMapClick,
  interactive = true,
}: MapViewProps) {
  return (
    <div className={`rounded-lg overflow-hidden border border-border ${className}`} style={{ height }}>
      <MapContainer
        center={center}
        zoom={zoom}
        scrollWheelZoom={interactive}
        dragging={interactive}
        zoomControl={interactive}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {onMapClick && <MapClickHandler onClick={onMapClick} />}

        {markers.map((m, i) => (
          <Marker
            key={i}
            position={m.position}
            icon={m.type === "driver" ? DriverIcon : DefaultIcon}
          >
            {m.label && <Popup>{m.label}</Popup>}
          </Marker>
        ))}

        {route && route.length > 1 && (
          <Polyline positions={route} pathOptions={{ color: "#0160CD", weight: 4, dashArray: "8 4" }} />
        )}

        {polygon && polygon.length > 2 && (
          <Polygon positions={polygon} pathOptions={{ color: "#0160CD", fillColor: "#0160CD", fillOpacity: 0.15 }} />
        )}

        {polygons?.map((p) => (
          <Polygon
            key={p.id}
            positions={p.coords}
            pathOptions={{
              color: p.color || "#0160CD",
              fillColor: p.color || "#0160CD",
              fillOpacity: 0.15,
              weight: 2,
            }}
          >
            {p.label && <Popup>{p.label}</Popup>}
          </Polygon>
        ))}
      </MapContainer>
    </div>
  );
}
