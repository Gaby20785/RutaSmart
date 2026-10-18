import { useCallback, useEffect, useState } from 'react'
import { api } from '../api.js'
import RouteMap from '../components/RouteMap.jsx'
import { fmt, formatDuration, hhmm, percent, routeColor, todayISO } from '../utils.js'

export default function RoutesPage() {
  const [date, setDate] = useState(todayISO())
  const [config, setConfig] = useState(null)
  const [plan, setPlan] = useState(null)
  const [pending, setPending] = useState([])
  const [highlight, setHighlight] = useState(null)
  const [expanded, setExpanded] = useState(null)
  const [balance, setBalance] = useState(true)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    api('/config').then(setConfig).catch((err) => setError(err.message))
  }, [])

  const load = useCallback(async () => {
    setError('')
    setHighlight(null)
    setExpanded(null)
    try {
      setPlan(await api(`/routes/plans?plan_date=${date}`))
      setPending([])
    } catch (err) {
      if (err.status !== 404) setError(err.message)
      setPlan(null)
      const orders = await api(`/orders?delivery_date=${date}`).catch(() => [])
      setPending(orders)
    }
  }, [date])

  useEffect(() => {
    load()
  }, [load])

  async function optimize() {
    setBusy(true)
    setError('')
    try {
      setPlan(await api('/routes/optimize', { method: 'POST', body: { plan_date: date, balance_workload: balance } }))
      setPending([])
      setHighlight(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  const toggleRoute = (id) => {
    setHighlight(highlight === id ? null : id)
    setExpanded(expanded === id ? null : id)
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Planificación de rutas</h1>
          <p className="muted">
            Salida y llegada: {config?.depot.name ?? '…'} · turno {hhmm(config?.shift_start)}–{hhmm(config?.shift_end)}
          </p>
        </div>
        <div className="toolbar">
          <label className="inline">
            Fecha
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          </label>
          <label className="checkbox" title="Reparte las paradas entre los conductores a cambio de algunos km más">
            <input type="checkbox" checked={balance} onChange={(e) => setBalance(e.target.checked)} />
            Equilibrar carga entre conductores
          </label>
          <button className="btn primary" onClick={optimize} disabled={busy}>
            {busy ? 'Optimizando…' : plan ? 'Volver a optimizar' : 'Optimizar rutas'}
          </button>
        </div>
      </div>

      {error && <div className="alert error">{error}</div>}

      {plan && (
        <div className="kpis">
          <div className="kpi">
            <span>Distancia total</span>
            <strong>{fmt(plan.total_distance_km)} km</strong>
          </div>
          <div className="kpi">
            <span>Sin optimizar</span>
            <strong className="muted-strong">{fmt(plan.baseline_distance_km)} km</strong>
          </div>
          <div className="kpi accent">
            <span>Ahorro</span>
            <strong>{fmt(plan.savings_pct)} %</strong>
          </div>
          <div className="kpi">
            <span>Pedidos planificados</span>
            <strong>{plan.orders_planned}</strong>
          </div>
          <div className="kpi">
            <span>Vehículos usados</span>
            <strong>{plan.vehicles_used}</strong>
          </div>
          <div className={`kpi ${plan.unassigned.length ? 'warn' : ''}`}>
            <span>Sin asignar</span>
            <strong>{plan.unassigned.length}</strong>
          </div>
        </div>
      )}

      <div className="routes-layout">
        <RouteMap depot={config?.depot} routes={plan?.routes ?? []} orders={plan ? [] : pending} highlight={highlight} />

        <aside className="routes-list">
          {!plan && (
            <div className="card empty-state">
              <h3>Sin rutas para esta fecha</h3>
              <p className="muted">
                {pending.length
                  ? `Hay ${pending.length} pedidos pendientes. Pulsa «Optimizar rutas» para generar el reparto.`
                  : 'No hay pedidos para esta fecha. Cárgalos en la pantalla de Pedidos.'}
              </p>
            </div>
          )}

          {plan?.routes.map((route, i) => (
            <div
              key={route.id}
              className={`card route-card ${highlight === route.id ? 'selected' : ''}`}
              style={{ borderLeftColor: routeColor(i) }}
            >
              <button className="route-head" onClick={() => toggleRoute(route.id)}>
                <span className="dot" style={{ background: routeColor(i) }} />
                <div className="route-title">
                  <strong>{route.vehicle.plate}</strong>
                  <span className="muted">{route.driver?.full_name ?? 'Sin conductor asignado'}</span>
                </div>
                <span className="chevron">{expanded === route.id ? '▾' : '▸'}</span>
              </button>
              <div className="route-stats">
                <span>{route.stops.length} paradas</span>
                <span>{fmt(route.distance_km)} km</span>
                <span>
                  {hhmm(route.start_time)}–{hhmm(route.end_time)} ({formatDuration(route.duration_min)})
                </span>
              </div>
              <div className="load">
                <div className="load-bar">
                  <div style={{ width: `${percent(route.load_kg, route.vehicle.capacity_kg)}%`, background: routeColor(i) }} />
                </div>
                <span className="muted">
                  Carga {fmt(route.load_kg, 0)} / {fmt(route.vehicle.capacity_kg, 0)} kg (
                  {percent(route.load_kg, route.vehicle.capacity_kg)} %) · {fmt(route.load_m3, 2)} /{' '}
                  {fmt(route.vehicle.capacity_m3, 1)} m³
                </span>
              </div>
              {expanded === route.id && (
                <ol className="stops">
                  {route.stops.map((s) => (
                    <li key={s.order.id}>
                      <span className="eta">{hhmm(s.eta)}</span>
                      <div>
                        <strong>{s.order.customer_name}</strong> <span className="muted mono">{s.order.reference}</span>
                        <br />
                        <span className="muted">
                          {s.order.address} · ventana {hhmm(s.order.window_start)}–{hhmm(s.order.window_end)}
                        </span>
                      </div>
                    </li>
                  ))}
                </ol>
              )}
            </div>
          ))}

          {plan?.unassigned.length > 0 && (
            <div className="card unassigned">
              <h3>Pedidos sin asignar</h3>
              <ul>
                {plan.unassigned.map((u) => (
                  <li key={u.order.id}>
                    <strong>{u.order.reference}</strong> — {u.reason}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </aside>
      </div>
    </div>
  )
}
