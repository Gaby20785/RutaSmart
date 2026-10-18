import { useCallback, useEffect, useRef, useState } from 'react'
import { api } from '../api.js'
import { hhmm, STATUS_LABELS, todayISO } from '../utils.js'

const emptyForm = (date) => ({
  reference: '',
  customer_name: '',
  customer_phone: '',
  address: '',
  lat: '',
  lng: '',
  delivery_date: date,
  window_start: '09:00',
  window_end: '14:00',
  weight_kg: '',
  volume_m3: '',
  service_minutes: 5,
})

export default function OrdersPage() {
  const [date, setDate] = useState(todayISO())
  const [orders, setOrders] = useState([])
  const [form, setForm] = useState(() => emptyForm(todayISO()))
  const [showForm, setShowForm] = useState(false)
  const [importResult, setImportResult] = useState(null)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [busy, setBusy] = useState(false)
  const fileInput = useRef(null)

  const load = useCallback(async () => {
    try {
      setOrders(await api(`/orders?delivery_date=${date}`))
    } catch (err) {
      setError(err.message)
    }
  }, [date])

  useEffect(() => {
    load()
  }, [load])

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value })

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setBusy(true)
    const body = {
      ...form,
      lat: form.lat === '' ? null : Number(form.lat),
      lng: form.lng === '' ? null : Number(form.lng),
      weight_kg: Number(form.weight_kg),
      volume_m3: Number(form.volume_m3),
      service_minutes: Number(form.service_minutes),
    }
    try {
      const created = await api('/orders', { method: 'POST', body })
      setNotice(`Pedido ${created.reference} creado`)
      setForm(emptyForm(date))
      setShowForm(false)
      if (created.delivery_date === date) load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function handleImport(e) {
    const file = e.target.files?.[0]
    if (!file) return
    setError('')
    setImportResult(null)
    setBusy(true)
    try {
      const result = await api('/orders/import', { method: 'POST', file })
      setImportResult(result)
      load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
      e.target.value = ''
    }
  }

  async function remove(order) {
    if (!window.confirm(`¿Eliminar el pedido ${order.reference}?`)) return
    try {
      await api(`/orders/${order.id}`, { method: 'DELETE' })
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  const totalKg = orders.reduce((acc, o) => acc + o.weight_kg, 0)
  const totalM3 = orders.reduce((acc, o) => acc + o.volume_m3, 0)

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Pedidos</h1>
          <p className="muted">
            {orders.length} pedidos · {totalKg.toLocaleString('es-ES', { maximumFractionDigits: 1 })} kg ·{' '}
            {totalM3.toLocaleString('es-ES', { maximumFractionDigits: 2 })} m³
          </p>
        </div>
        <div className="toolbar">
          <label className="inline">
            Fecha
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          </label>
          <button className="btn ghost" onClick={() => fileInput.current?.click()} disabled={busy}>
            Importar CSV
          </button>
          <input ref={fileInput} type="file" accept=".csv,text/csv" hidden onChange={handleImport} />
          <button
            className="btn primary"
            onClick={() => {
              setForm(emptyForm(date))
              setShowForm(!showForm)
            }}
          >
            {showForm ? 'Cerrar' : 'Nuevo pedido'}
          </button>
        </div>
      </div>

      {notice && <div className="alert success" onClick={() => setNotice('')}>{notice}</div>}
      {error && <div className="alert error">{error}</div>}

      {importResult && (
        <div className={`alert ${importResult.errors.length ? 'warning' : 'success'}`}>
          <strong>{importResult.created} pedidos importados.</strong>
          {importResult.errors.length > 0 && (
            <>
              {' '}
              {importResult.errors.length} filas con errores (no se han importado):
              <ul>
                {importResult.errors.map((e) => (
                  <li key={e.row}>
                    Fila {e.row}
                    {e.reference ? ` (${e.reference})` : ''}: {e.error}
                  </li>
                ))}
              </ul>
            </>
          )}
          <button className="link" onClick={() => setImportResult(null)}>
            Cerrar
          </button>
        </div>
      )}

      {showForm && (
        <form className="card form" onSubmit={handleSubmit}>
          <h2>Nuevo pedido</h2>
          <div className="row">
            <label>
              Referencia
              <input value={form.reference} onChange={set('reference')} required maxLength={40} />
            </label>
            <label>
              Cliente
              <input value={form.customer_name} onChange={set('customer_name')} required minLength={2} />
            </label>
            <label>
              Teléfono
              <input value={form.customer_phone} onChange={set('customer_phone')} />
            </label>
          </div>
          <label>
            Dirección
            <input value={form.address} onChange={set('address')} required minLength={5} placeholder="Calle, número, ciudad" />
          </label>
          <div className="row">
            <label>
              Latitud (opcional)
              <input type="number" step="any" value={form.lat} onChange={set('lat')} placeholder="Se geocodifica si se deja vacía" />
            </label>
            <label>
              Longitud (opcional)
              <input type="number" step="any" value={form.lng} onChange={set('lng')} />
            </label>
            <label>
              Fecha de entrega
              <input type="date" value={form.delivery_date} onChange={set('delivery_date')} required />
            </label>
          </div>
          <div className="row">
            <label>
              Ventana desde
              <input type="time" value={form.window_start} onChange={set('window_start')} required />
            </label>
            <label>
              Ventana hasta
              <input type="time" value={form.window_end} onChange={set('window_end')} required />
            </label>
            <label>
              Peso (kg)
              <input type="number" min="0.1" step="any" value={form.weight_kg} onChange={set('weight_kg')} required />
            </label>
            <label>
              Volumen (m³)
              <input type="number" min="0.001" step="any" value={form.volume_m3} onChange={set('volume_m3')} required />
            </label>
            <label>
              Servicio (min)
              <input type="number" min="1" max="120" value={form.service_minutes} onChange={set('service_minutes')} />
            </label>
          </div>
          <div className="actions">
            <button className="btn primary" disabled={busy}>
              {busy ? 'Guardando…' : 'Crear pedido'}
            </button>
          </div>
        </form>
      )}

      <div className="card table-card">
        <table>
          <thead>
            <tr>
              <th>Referencia</th>
              <th>Cliente</th>
              <th>Dirección</th>
              <th>Ventana</th>
              <th className="num">kg</th>
              <th className="num">m³</th>
              <th>Estado</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {orders.map((o) => (
              <tr key={o.id}>
                <td className="mono">{o.reference}</td>
                <td>{o.customer_name}</td>
                <td className="truncate" title={o.address}>
                  {o.address}
                </td>
                <td className="mono">
                  {hhmm(o.window_start)}–{hhmm(o.window_end)}
                </td>
                <td className="num">{o.weight_kg}</td>
                <td className="num">{o.volume_m3}</td>
                <td>
                  <span className={`badge ${o.status}`}>{STATUS_LABELS[o.status]}</span>
                </td>
                <td className="row-actions">
                  {o.status === 'pending' && (
                    <button className="btn danger small" onClick={() => remove(o)}>
                      Eliminar
                    </button>
                  )}
                </td>
              </tr>
            ))}
            {orders.length === 0 && (
              <tr>
                <td colSpan={8} className="empty">
                  No hay pedidos para esta fecha. Crea uno o importa un CSV.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
