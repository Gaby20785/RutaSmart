import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth-context.js'
import { homePathFor } from '../utils.js'

const DEMO_USERS = [
  { label: 'Admin', email: 'admin@rutasmart.dev', password: 'Admin1234' },
  { label: 'Despachador', email: 'despacho@rutasmart.dev', password: 'Despacho1234' },
  { label: 'Conductor', email: 'conductor1@rutasmart.dev', password: 'Conductor1234' },
]

export default function LoginPage() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  if (user) return <Navigate to={homePathFor(user.role)} replace />

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      const logged = await login(email, password)
      navigate(homePathFor(logged.role), { replace: true })
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleSubmit}>
        <div className="brand big">
          <span className="brand-mark">R</span>
          <span>RutaSmart</span>
        </div>
        <p className="muted">Optimizador de rutas de entrega</p>
        <label>
          Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoFocus />
        </label>
        <label>
          Contraseña
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        {error && <div className="alert error">{error}</div>}
        <button className="btn primary" disabled={busy}>
          {busy ? 'Entrando…' : 'Entrar'}
        </button>
        <div className="demo-users">
          <span className="muted">Usuarios de demo:</span>
          {DEMO_USERS.map((u) => (
            <button
              type="button"
              key={u.email}
              className="btn ghost small"
              onClick={() => {
                setEmail(u.email)
                setPassword(u.password)
              }}
            >
              {u.label}
            </button>
          ))}
        </div>
      </form>
    </div>
  )
}
