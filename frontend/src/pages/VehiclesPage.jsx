import { useCallback, useEffect, useState } from 'react'
import { api } from '../api.js'
import { useAuth } from '../auth-context.js'

const EMPTY = { plate: '', model: '', capacity_kg: '', capacity_m3: '', driver_id: '' }

export default function VehiclesPage() {
  const { user } = useAuth()
  const isAdmin = user.role === 'admin'
  const [vehicles, setVehicles] = useState([])
  const [drivers, setDrivers] = useState([])
  const [form, setForm] = useState(EMPTY)
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  const load = useCallback(async () => {
    try {
      const [v, d] = await Promise.all([api('/vehicles'), api('/drivers')])
      setVehicles(v)
      setDrivers(d)
    } catch (err) {
      setError(err.message)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load])

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value })

  function startEdit(v) {
    setEditingId(v.id)
    setForm({
      plate: v.plate,
      model: v.model,
      capacity_kg: v.capacity_kg,
      capacity_m3: v.capacity_m3,
      driver_id: v.driver?.id ?? '',
    })
    setError('')
  }

  function cancelEdit() {
    setEditingId(null)
    setForm(EMPTY)
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    const body = {
      plate: form.plate,
      model: form.model,
      capacity_kg: Number(form.capacity_kg),
      capacity_m3: Number(form.capacity_m3),
      driver_id: form.driver_id ? Number(form.driver_id) : null,
    }
    try {
      if (editingId) await api(`/vehicles/${editingId}`, { method: 'PUT', body })
      else await api('/vehicles', { method: 'POST', body })
      setNotice(editingId ? 'Vehículo actualizado' : 'Vehículo dado de alta')
      cancelEdit()
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  async function deactivate(v) {
    if (!window.confirm(`¿Dar de baja el vehículo ${v.plate}?`)) return
    try {
      await api(`/vehicles/${v.id}`, { method: 'DELETE' })
      setNotice(`Vehículo ${v.plate} dado de baja`)
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  const totalKg = vehicles.reduce((acc, v) => acc + v.capacity_kg, 0)
  const totalM3 = vehicles.reduce((acc, v) => acc + v.capacity_m3, 0)

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Vehículos</h1>
          <p className="muted">
            {vehicles.length} vehículos activos · capacidad total {totalKg.toLocaleString('es-ES')} kg ·{' '}
            {totalM3.toLocaleString('es-ES')} m³
          </p>
        </div>
      </div>

      {notice && <div className="alert success" onClick={() => setNotice('')}>{notice}</div>}
      {error && <div className="alert error">{error}</div>}

      <div className={isAdmin ? 'grid-2' : ''}>
        {isAdmin && (
          <form className="card form" onSubmit={handleSubmit}>
            <h2>{editingId ? 'Editar vehículo' : 'Nuevo vehículo'}</h2>
            <label>
              Matrícula
              <input value={form.plate} onChange={set('plate')} required minLength={4} maxLength={15} placeholder="1234ABC" />
            </label>
            <label>
              Modelo
              <input value={form.model} onChange={set('model')} maxLength={80} placeholder="Renault Kangoo" />
            </label>
            <div className="row">
              <label>
                Capacidad (kg)
                <input type="number" min="1" step="any" value={form.capacity_kg} onChange={set('capacity_kg')} required />
              </label>
              <label>
                Capacidad (m³)
                <input type="number" min="0.1" step="any" value={form.capacity_m3} onChange={set('capacity_m3')} required />
              </label>
            </div>
            <label>
              Conductor habitual
              <select value={form.driver_id} onChange={set('driver_id')}>
                <option value="">— Sin asignar —</option>
                {drivers.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.full_name}
                  </option>
                ))}
              </select>
            </label>
            <div className="actions">
              <button className="btn primary">{editingId ? 'Guardar cambios' : 'Dar de alta'}</button>
              {editingId && (
                <button type="button" className="btn ghost" onClick={cancelEdit}>
                  Cancelar
                </button>
              )}
            </div>
          </form>
        )}

        <div className="card table-card">
          <table>
            <thead>
              <tr>
                <th>Matrícula</th>
                <th>Modelo</th>
                <th className="num">kg</th>
                <th className="num">m³</th>
                <th>Conductor</th>
                {isAdmin && <th />}
              </tr>
            </thead>
            <tbody>
              {vehicles.map((v) => (
                <tr key={v.id}>
                  <td className="mono">{v.plate}</td>
                  <td>{v.model}</td>
                  <td className="num">{v.capacity_kg.toLocaleString('es-ES')}</td>
                  <td className="num">{v.capacity_m3.toLocaleString('es-ES')}</td>
                  <td>{v.driver?.full_name ?? <span className="muted">—</span>}</td>
                  {isAdmin && (
                    <td className="row-actions">
                      <button className="btn ghost small" onClick={() => startEdit(v)}>
                        Editar
                      </button>
                      <button className="btn danger small" onClick={() => deactivate(v)}>
                        Baja
                      </button>
                    </td>
                  )}
                </tr>
              ))}
              {vehicles.length === 0 && (
                <tr>
                  <td colSpan={6} className="empty">
                    No hay vehículos dados de alta
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
