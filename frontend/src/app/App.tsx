import { lazy, Suspense } from 'react'
import { BrowserRouter, Navigate, Outlet, Route, Routes } from 'react-router-dom'
import { getAccessToken } from '../api/client'
import { ActivitiesPage } from '../pages/ActivitiesPage'
import { AuthPage } from '../pages/AuthPage'
import { CentersPage, NearbyCenterPage } from '../pages/CentersPage'
import { DiagnosisPage, DiagnosisResultPage, MeasurementInputPage } from '../pages/DiagnosisPages'
import { DashboardPage, HomePage, OnboardingPage, RegionalPage } from '../pages/MainPages'
import { useCurrentUser } from '../hooks/useAuth'

const RecordsPage = lazy(() => import('../pages/RecordsPages').then(({ RecordsPage: Page }) => ({ default: Page })))
const GrowthPage = lazy(() => import('../pages/RecordsPages').then(({ GrowthPage: Page }) => ({ default: Page })))
const MeasurementDetailPage = lazy(() => import('../pages/RecordsPages').then(({ MeasurementDetailPage: Page }) => ({ default: Page })))

function RouteLoading() {
  return (
    <div className="grid min-h-[50vh] place-items-center text-sm text-on-surface-variant" role="status">
      화면을 준비하고 있어요…
    </div>
  )
}

function ProtectedRoutes() {
  const token = getAccessToken()
  const userQuery = useCurrentUser()

  if (!token) return <Navigate to="/login" replace />
  if (userQuery.isPending) return <RouteLoading />
  if (userQuery.isError) return <Navigate to="/login" replace />
  return <Outlet />
}

export function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<RouteLoading />}>
        <Routes>
          <Route path="/login" element={<AuthPage mode="login" />} />
          <Route path="/signup" element={<AuthPage mode="signup" />} />
          <Route element={<ProtectedRoutes />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/onboarding" element={<OnboardingPage />} />
            <Route path="/home" element={<HomePage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/diagnosis" element={<DiagnosisPage />} />
            <Route path="/diagnosis/input" element={<MeasurementInputPage />} />
            <Route path="/diagnosis/result" element={<DiagnosisResultPage />} />
            <Route path="/records/:measurementId" element={<MeasurementDetailPage />} />`r`n            <Route path="/records" element={<RecordsPage />} />
            <Route path="/growth" element={<GrowthPage />} />
            <Route path="/activities" element={<ActivitiesPage />} />
            <Route path="/centers" element={<CentersPage />} />
            <Route path="/centers/nearby" element={<NearbyCenterPage />} />
            <Route path="/regional" element={<RegionalPage />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}