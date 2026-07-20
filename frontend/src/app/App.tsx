import { lazy, Suspense } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { ActivitiesPage } from '../pages/ActivitiesPage'
import { CentersPage, NearbyCenterPage } from '../pages/CentersPage'
import { DiagnosisPage, DiagnosisResultPage, MeasurementInputPage } from '../pages/DiagnosisPages'
import { DashboardPage, HomePage, OnboardingPage, RegionalPage } from '../pages/MainPages'

const RecordsPage = lazy(() => import('../pages/RecordsPages').then(({ RecordsPage: Page }) => ({ default: Page })))
const GrowthPage = lazy(() => import('../pages/RecordsPages').then(({ GrowthPage: Page }) => ({ default: Page })))

function RouteLoading() {
  return (
    <div className="grid min-h-[50vh] place-items-center text-sm text-on-surface-variant" role="status">
      화면을 준비하고 있어요…
    </div>
  )
}

export function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<RouteLoading />}>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/diagnosis" element={<DiagnosisPage />} />
          <Route path="/diagnosis/input" element={<MeasurementInputPage />} />
          <Route path="/diagnosis/result" element={<DiagnosisResultPage />} />
          <Route path="/records" element={<RecordsPage />} />
          <Route path="/growth" element={<GrowthPage />} />
          <Route path="/activities" element={<ActivitiesPage />} />
          <Route path="/centers" element={<CentersPage />} />
          <Route path="/centers/nearby" element={<NearbyCenterPage />} />
          <Route path="/regional" element={<RegionalPage />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}
