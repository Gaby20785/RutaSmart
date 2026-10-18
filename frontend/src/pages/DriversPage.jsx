import { useCallback, useEffect, useState } from 'react'
import { api } from '../api.js'
import { useAuth } from '../auth-context.js'

const EMPTY = { full_name: '', phone: '', license_number: '', email: '', password: '' }

export default function DriversPage() {
  const { user } = useAuth()
  const isAdmin = user.role === 'admin'
  const [drivers, setDrivers] = useState([])
  const [form, setForm] = useState(EMPTY)
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  const load = useCallback(async () => {
    try {
      setDrivers(await api('/drivers'))
    } catch (err) {
      setError(err.message)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load])

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value })

  function startEdit(d) {
    setEditingId(d.id)
    setForm({ ...EMPTY, full_name: d.full_name, phone: d.phone, license_number: d.license_number })
    setError('')
  }

  function cancelEdit() {
    setEditingId(null)
    setForm(EMPTY)
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    const body = { full_name: form.full_name, phone: form.phone, license_number: form.license_number }
    try {
      if (editingId) {
        await api(`/drivers/${editingId}`, { method: 'PUT', body })
      } else {
        if (form.email || form.password) Object.assign(body, { email: form.email, password: form.password })
        await api('/drivers', { method: 'POST', body })
      }
      setNotice(editingId ? 'Conductor actualizado' : 'Conductor dado de alta')
      cancelEdit()
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  async function deactivate(d) {
    if (!window.confirm(`¿Dar de baja a ${d.full_name}?`)) return
    try {
      await api(`/drivers/${d.id}`, { method: 'DELETE' })
      setNotice(`${d.full_name} dado de baja`)
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Conductores</h1>
          <p className="muted">{drivers.length} conductores activos</p>
        </div>
      </div>

      {notice && <div className="alert success" onClick={() => setNotice('')}>{notice}</div>}
      {error && <div className="alert error">{error}</div>}

      <div className={isAdmin ? 'grid-2' : ''}>
        {isAdmin && (
          <form className="card form" onSubmit={handleSubmit}>
            <h2>{editingId ? 'Editar conductor' : 'Nuevo conductor'}</h2>
            <label>
              Nombre completo
              <input value={form.full_name} onChange={set('full_name')} required minLength={2} />
            </label>
            <div className="row">
              <label>
                Teléfono
                <input value={form.phone} onChange={set('phone')} required minLength={6} />
              </label>
              <label>
                Nº de licencia
                <input value={form.license_number} onChange={set('license_number')} required minLength={3} />
              </label>
            </div>
            {!editingId && (
              <fieldset>
                <legend>Cuenta para la app (opcional)</legend>
                <div className="row">
                  <label>
                    Email
                    <input type="email" value={form.email} onChange={set('email')} />
                  </label>
                  <label>
                    Contraseña
                    <input type="password" value={form.password} onChange={set('password')} minLength={8} />
                  </label>
                </div>
              </fieldset>
            )}
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
                <th>Nombre</th>
                <th>Teléfono</th>
                <th>Licencia</th>
                <th>Acceso app</th>
                {isAdmin && <th />}
              </tr>
            </thead>
            <tbody>
              {drivers.map((d) => (
                <tr key={d.id}>
                  <td>{d.full_name}</td>
                  <td>{d.phone}</td>
                  <td className="mono">{d.license_number}</td>
                  <td>{d.user_id ? <span className="badge planned">Sí</span> : <span className="muted">No</span>}</td>
                  {isAdmin && (
                    <td className="row-actions">
                      <button className="btn ghost small" onClick={() => startEdit(d)}>
                        Editar
                      </button>
                      <button className="btn danger small" onClick={() => deactivate(d)}>
                        Baja
                      </button>
                    </td>
                  )}
                </tr>
              ))}
              {drivers.length === 0 && (
                <tr>
                  <td colSpan={5} className="empty">
                    No hay conductores dados de alta
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
