const TOKEN_KEY = 'rutasmart_token'

export function getToken() {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setToken(token) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  } catch {
    // almacenamiento no disponible (modo privado): la sesión dura lo que la pestaña
  }
}

export class ApiError extends Error {
  constructor(status, message) {
    super(message)
    this.status = status
  }
}

/** Convierte el `detail` de FastAPI (texto o lista de errores de validación) en un mensaje legible. */
export function errorMessage(body, fallback) {
  const detail = body?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((e) => {
        const field = (e.loc || []).slice(1).join('.')
        const msg = String(e.msg).replace(/^Value error, /, '')
        return field ? `${field}: ${msg}` : msg
      })
      .join(' · ')
  }
  return fallback
}

export async function api(path, { method = 'GET', body, form, file } = {}) {
  const headers = {}
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  let payload
  if (form) {
    payload = new URLSearchParams(form)
  } else if (file) {
    payload = new FormData()
    payload.append('file', file)
  } else if (body !== undefined) {
    headers['Content-Type'] = 'application/json'
    payload = JSON.stringify(body)
  }

  const response = await fetch(`/api${path}`, { method, headers, body: payload })
  if (response.status === 401 && token) {
    setToken(null)
    window.dispatchEvent(new Event('rutasmart:logout'))
  }
  if (response.status === 204) return null
  const data = await response.json().catch(() => null)
  if (!response.ok) throw new ApiError(response.status, errorMessage(data, `Error ${response.status}`))
  return data
}
