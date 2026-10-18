import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import AuthProvider from './AuthProvider.jsx'
import { useAuth } from './auth-context.js'
import Layout from './components/Layout.jsx'
import DriversPage from './pages/DriversPage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import MyRoutesPage from './pages/MyRoutesPage.jsx'
import OrdersPage from './pages/OrdersPage.jsx'
import RoutesPage from './pages/RoutesPage.jsx'
import VehiclesPage from './pages/VehiclesPage.jsx'
import { homePathFor } from './utils.js'

function RequireRole({ roles, children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="center-screen">Cargando…</div>
  if (!user) return <Navigate to="/login" replace />
  if (roles && !roles.includes(user.role)) return <Navigate to={homePathFor(user.role)} replace />
  return children
}

function Home() {
  const { user } = useAuth()
  return <Navigate to={homePathFor(user?.role)} replace />
}

const STAFF = ['admin', 'dispatcher']

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            element={
              <RequireRole>
                <Layout />
              </RequireRole>
            }
          >
            <Route index element={<Home />} />
            <Route path="vehiculos" element={<RequireRole roles={STAFF}><VehiclesPage /></RequireRole>} />
            <Route path="conductores" element={<RequireRole roles={STAFF}><DriversPage /></RequireRole>} />
            <Route path="pedidos" element={<RequireRole roles={STAFF}><OrdersPage /></RequireRole>} />
            <Route path="rutas" element={<RequireRole roles={STAFF}><RoutesPage /></RequireRole>} />
            <Route path="mis-rutas" element={<RequireRole roles={['driver']}><MyRoutesPage /></RequireRole>} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
