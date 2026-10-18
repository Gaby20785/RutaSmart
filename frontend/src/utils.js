export const ROUTE_COLORS = ['#e8590c', '#1971c2', '#2f9e44', '#9c36b5', '#f08c00', '#0c8599', '#c2255c', '#5c940d']

export const routeColor = (index) => ROUTE_COLORS[index % ROUTE_COLORS.length]

export const hhmm = (t) => (t ? t.slice(0, 5) : '')

export const ROLE_LABELS = { admin: 'Administrador', dispatcher: 'Despachador', driver: 'Conductor' }

export const STATUS_LABELS = {
  pending: 'Pendiente',
  planned: 'Planificado',
  delivered: 'Entregado',
  failed: 'Fallido',
}

export function formatDuration(minutes) {
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  return h ? `${h} h ${String(m).padStart(2, '0')} min` : `${m} min`
}

export function fmt(n, digits = 1) {
  return Number(n).toLocaleString('es-ES', { minimumFractionDigits: digits, maximumFractionDigits: digits })
}

export function todayISO() {
  const d = new Date()
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  return d.toISOString().slice(0, 10)
}

export function percent(value, total) {
  return total > 0 ? Math.round((value / total) * 100) : 0
}

export const homePathFor = (role) => ({ admin: '/vehiculos', dispatcher: '/rutas', driver: '/mis-rutas' })[role] || '/login'
