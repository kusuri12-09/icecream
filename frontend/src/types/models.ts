export type Grade = '씨앗' | '새싹' | '꽃' | '열매'
export type MeasurementType = 'official' | 'self'

export interface ChildProfile {
  id: string
  name: string
  ageLabel: string
  gender: 'male' | 'female'
  avatarIcon: string
}

export interface MeasurementRecord {
  id: string
  date: string
  type: MeasurementType
  grade: Grade
  score: number
  strengths: string[]
  needsWork: string[]
}

export interface Activity {
  id: string
  title: string
  category: string
  place: '실내' | '야외'
  duration: string
  icon: string
  description: string
  equipment: boolean
}

export interface Center {
  id: string
  name: string
  address: string
  distance: string
  icon: string
  open: boolean
}
