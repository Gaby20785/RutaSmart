import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../auth-context.js'
import { ROLE_LABELS } from '../utils.js'

const LINKS = [
  { to: '/rutas', label: 'Rutas', roles: ['admin', 'dispatcher'] },
  { to: '/pedidos', label: 'Pedidos', roles: ['admin', 'dispatcher'] },
  { to: '/vehiculos', label: 'Vehículos', roles: ['admin', 'dispatcher'] },
  { to: '/conductores', label: 'Conductores', roles: ['admin', 'dispatcher'] },
  { to: '/mis-rutas', label: 'Mis rutas', roles: ['driver'] },
]

export default function Layout() {
  const { user, logout } = useAuth()
  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">R</span>
          <span>RutaSmart</span>
        </div>
        <nav className="nav">
          {LINKS.filter((l) => l.roles.includes(user.role)).map((l) => (
            <NavLink key={l.to} to={l.to} className={({ isActive }) => (isActive ? 'active' : '')}>
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className="user">
          <div className="user-info">
            <strong>{user.full_name}</strong>
            <span>{ROLE_LABELS[user.role]}</span>
          </div>
          <button className="btn ghost small" onClick={logout}>
            Salir
          </button>
        </div>
      </header>
      <main className="content">
        <Outlet />
      </main>
    </div>
  )
}
