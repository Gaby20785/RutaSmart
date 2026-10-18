import L from 'leaflet'
import { Fragment, useEffect, useMemo } from 'react'
import { MapContainer, Marker, Polyline, Popup, TileLayer, useMap } from 'react-leaflet'
import { hhmm, routeColor } from '../utils.js'

function numberedIcon(label, color) {
  return L.divIcon({
    className: 'stop-icon',
    html: `<span style="background:${color}">${label}</span>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  })
}

const depotIcon = L.divIcon({
  className: 'depot-icon',
  html: '<span>A</span>',
  iconSize: [30, 30],
  iconAnchor: [15, 15],
})

function FitBounds({ points }) {
  const map = useMap()
  useEffect(() => {
    if (points.length > 1) map.fitBounds(points, { padding: [30, 30] })
    else if (points.length === 1) map.setView(points[0], 13)
  }, [map, points])
  return null
}

/**
 * Mapa de rutas. Las líneas unen las paradas en orden (trazado recto);
 * el trazado por calles llega con la integración de Mapbox (RF17, Sprint 2).
 */
export default function RouteMap({ depot, routes = [], orders = [], highlight = null }) {
  const points = useMemo(() => {
    const pts = depot ? [[depot.lat, depot.lng]] : []
    routes.forEach((r) => r.stops.forEach((s) => pts.push([s.order.lat, s.order.lng])))
    orders.forEach((o) => pts.push([o.lat, o.lng]))
    return pts
  }, [depot, routes, orders])

  if (!depot) return <div className="map placeholder">Cargando mapa…</div>

  return (
    <MapContainer className="map" center={[depot.lat, depot.lng]} zoom={12} scrollWheelZoom>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <FitBounds points={points} />
      <Marker position={[depot.lat, depot.lng]} icon={depotIcon}>
        <Popup>
          <strong>{depot.name}</strong>
          <br />
          Salida y llegada de todas las rutas
        </Popup>
      </Marker>

      {routes.map((route, i) => {
        const color = routeColor(i)
        const dimmed = highlight !== null && highlight !== route.id
        const path = [[depot.lat, depot.lng], ...route.stops.map((s) => [s.order.lat, s.order.lng]), [depot.lat, depot.lng]]
        return (
          <Fragment key={route.id}>
            <Polyline positions={path} pathOptions={{ color, weight: dimmed ? 2 : 4, opacity: dimmed ? 0.25 : 0.85 }} />
            {!dimmed &&
              route.stops.map((s) => (
                <Marker key={s.order.id} position={[s.order.lat, s.order.lng]} icon={numberedIcon(s.sequence, color)}>
                  <Popup>
                    <strong>
                      #{s.sequence} · {s.order.reference}
                    </strong>
                    <br />
                    {s.order.customer_name}
                    <br />
                    {s.order.address}
                    <br />
                    ETA <strong>{hhmm(s.eta)}</strong> · ventana {hhmm(s.order.window_start)}–{hhmm(s.order.window_end)}
                    <br />
                    {s.order.weight_kg} kg · {s.order.volume_m3} m³
                  </Popup>
                </Marker>
              ))}
          </Fragment>
        )
      })}

      {orders.map((o) => (
        <Marker key={o.id} position={[o.lat, o.lng]} icon={numberedIcon('•', '#868e96')}>
          <Popup>
            <strong>{o.reference}</strong>
            <br />
            {o.address}
            <br />
            Ventana {hhmm(o.window_start)}–{hhmm(o.window_end)}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}
