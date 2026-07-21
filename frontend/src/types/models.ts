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