import { useEffect, useState } from 'react'
import { api } from '../api.js'
import RouteMap from '../components/RouteMap.jsx'
import { fmt, hhmm, todayISO } from '../utils.js'

/** Vista mínima del conductor. La app completa del repartidor (PWA) llega en el Sprint 2. */
export default function MyRoutesPage() {
  const [date, setDate] = useState(todayISO())
  const [config, setConfig] = useState(null)
  const [routes, setRoutes] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    api('/config').then(setConfig).catch((err) => setError(err.message))
  }, [])

  useEffect(() => {
    api(`/routes/mine?plan_date=${date}`)
      .then(setRoutes)
      .catch((err) => setError(err.message))
  }, [date])

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Mis rutas</h1>
          <p className="muted">Ruta asignada para el día seleccionado</p>
        </div>
        <label className="inline">
          Fecha
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        </label>
      </div>
      {error && <div className="alert error">{error}</div>}
      {routes.length === 0 ? (
        <div className="card empty-state">
          <h3>No tienes rutas asignadas para este día</h3>
        </div>
      ) : (
        <div className="routes-layout">
          <RouteMap depot={config?.depot} routes={routes} />
          <aside className="routes-list">
            {routes.map((route) => (
              <div key={route.id} className="card route-card">
                <div className="route-stats">
                  <strong>{route.vehicle.plate}</strong>
                  <span>{route.stops.length} paradas</span>
                  <span>{fmt(route.distance_km)} km</span>
                  <span>
                    Salida {hhmm(route.start_time)} · vuelta {hhmm(route.end_time)}
                  </span>
                </div>
                <ol className="stops">
                  {route.stops.map((s) => (
                    <li key={s.order.id}>
                      <span className="eta">{hhmm(s.eta)}</span>
                      <div>
                        <strong>{s.order.customer_name}</strong>
                        <br />
                        <span className="muted">{s.order.address}</span>
                      </div>
                    </li>
                  ))}
                </ol>
              </div>
            ))}
          </aside>
        </div>
      )}
    </div>
  )
}
