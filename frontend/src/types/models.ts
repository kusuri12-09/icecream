export type Grade = '씨앗' | '새싹' | '꽃' | '열매'
export type MeasurementType = 'official' | 'self'

export interface ChildProfile {
  id: string
  name: string
  ageLabel: string
  ageMonths?: number
  gender: 'male' | 'female'
  avatarIcon: string
  birthYearMonth?: string
  inTargetRange?: boolean
}

export interface MeasurementRecord {
  id: string
  date: string
  measuredAt?: string
  type: MeasurementType
  grade: Grade
  score?: number
  strengths: string[]
  needsWork: string[]
}

export interface MeasurementRequest {
  type: 'OFFICIAL' | 'SELF'
  measuredAt: string
  centerId?: string | null
  items: Array<{ itemKey: string; value: number }>
}

export interface MeasurementItemResult {
  itemKey: string
  label: string
  value: number
  itemGrade?: Grade
  isWeak: boolean
}

export interface MeasurementResult {
  id: string
  childId: string
  type: MeasurementType
  measuredAt: string
  ageMonthsAtMeasure?: number
  grade: Grade
  center?: { id: string; name: string } | null
  items: MeasurementItemResult[]
  profile: { strengths: string[]; weaknesses: string[]; undecidableGrades: string[] }
  createdAt?: string
}
export interface Activity {
  id: string
  title: string
  category: string
  place?: '실내' | '야외'
  duration?: string
  icon: string
  description: string
  equipment?: boolean
  url?: string
}

export interface Center {
  id: string
  name: string
  address: string
  distance: string
  icon: string
  open: boolean
  reservationUrl?: string
  stale?: boolean
}

export interface GrowthPoint {
  measuredAt: string
  value: number
  type: 'OFFICIAL' | 'SELF'
}

export interface GrowthSeries {
  itemKey: string
  label: string
  unit: string
  points: GrowthPoint[]
}

export interface GrowthData {
  childId: string
  series: GrowthSeries[]
  gradeHistory: Array<{ measuredAt: string; grade: string }>
}
export interface RegionalInsight {
  region: string
  regionMeasureCount: number
  nationalAvg: number
  relativeLevel: string
  percentile?: number
  message: string
  cta?: { type: string; label: string }
}

export interface RegionalRegion {
  sidoSigungu: string
  measureCount: number
  participationRate: number
}