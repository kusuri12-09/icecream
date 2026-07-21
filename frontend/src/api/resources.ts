import { apiRequest, unwrapData } from './client'
import type { Activity, Center, ChildProfile, MeasurementRecord, RegionalInsight, RegionalRegion, GrowthData } from '../types/models'

const gradeNames: Record<string, MeasurementRecord['grade']> = {
  SEED: '씨앗',
  SPROUT: '새싹',
  FLOWER: '꽃',
  FRUIT: '열매',
}

export async function getChildren() {
  const response = await apiRequest<unknown>('/api/v1/children')
  const data = unwrapData<{ items?: unknown[] }>(response)
  return (data.items ?? []).map(mapChild)
}

export async function createChild(input: { nickname: string; gender: 'MALE' | 'FEMALE'; birthYearMonth: string }) {
  const response = await apiRequest<unknown>('/api/v1/children', {
    method: 'POST',
    body: JSON.stringify(input),
  })
  return mapChild(unwrapData<unknown>(response))
}

export async function updateChild(
  childId: string,
  input: Partial<{ nickname: string; gender: 'MALE' | 'FEMALE'; birthYearMonth: string }>,
) {
  const response = await apiRequest<unknown>(`/api/v1/children/${childId}`, {
    method: 'PATCH',
    body: JSON.stringify(input),
  })
  return mapChild(unwrapData<unknown>(response))
}
export async function getChild(childId: string) {
  const response = await apiRequest<unknown>(`/api/v1/children/${childId}`)
  return mapChild(unwrapData<unknown>(response))
}

export async function getMeasurements(childId: string) {
  const response = await apiRequest<unknown>(`/api/v1/children/${childId}/measurements`)
  const data = unwrapData<{ items?: unknown[] }>(response)
  return (data.items ?? []).map(mapMeasurement)
}

export async function getMeasurement(measurementId: string) {
  const response = await apiRequest<unknown>(`/api/v1/measurements/${measurementId}`)
  return mapMeasurement(unwrapData<unknown>(response))
}

export async function getGrowth(childId: string, itemKey?: string): Promise<GrowthData> {
  const query = itemKey ? `?itemKey=${encodeURIComponent(itemKey)}` : ''
  const response = await apiRequest<unknown>(`/api/v1/children/${childId}/growth${query}`)
  return unwrapData<GrowthData>(response)
}

export async function getActivities() {
  const response = await apiRequest<unknown>('/api/v1/activities')
  const data = unwrapData<{ items?: unknown[] }>(response)
  return (data.items ?? []).map(mapActivity)
}

export async function getCenters() {
  const response = await apiRequest<unknown>('/api/v1/centers')
  const data = unwrapData<{ items?: unknown[] }>(response)
  return (data.items ?? []).map(mapCenter)
}

export async function getRegionalInsight(sidoSigungu?: string) {
  const query = sidoSigungu ? `?sidoSigungu=${encodeURIComponent(sidoSigungu)}` : ''
  const response = await apiRequest<unknown>(`/api/v1/insights/regional${query}`)
  return unwrapData<RegionalInsight>(response)
}

export async function getRegionalMap() {
  const response = await apiRequest<unknown>('/api/v1/insights/regional/map')
  const data = unwrapData<{ regions?: RegionalRegion[] }>(response)
  return data.regions ?? []
}

function mapChild(value: unknown): ChildProfile {
  const child = asRecord(value)
  const ageMonths = typeof child.ageMonths === 'number' ? child.ageMonths : undefined
  const gender = child.gender === 'FEMALE' || child.gender === 'female' ? 'female' : 'male'
  return {
    id: stringValue(child.id),
    name: stringValue(child.nickname ?? child.name, '아이'),
    ageLabel: ageMonths == null ? '' : `만 ${Math.floor(ageMonths / 12)}세 · ${ageMonths}개월`,
    ageMonths,
    gender,
    avatarIcon: gender === 'female' ? 'girl' : 'boy',
    birthYearMonth: stringValue(child.birthYearMonth),
    inTargetRange: typeof child.inTargetRange === 'boolean' ? child.inTargetRange : undefined,
  }
}

function mapMeasurement(value: unknown): MeasurementRecord {
  const measurement = asRecord(value)
  const grade = gradeNames[stringValue(measurement.grade).toUpperCase()] ?? '씨앗'
  const measuredAt = stringValue(measurement.measuredAt)
  return {
    id: stringValue(measurement.id),
    date: measuredAt ? new Date(measuredAt).toLocaleDateString('ko-KR') : '-',
    measuredAt,
    type: stringValue(measurement.type).toUpperCase() === 'SELF' ? 'self' : 'official',
    grade,
    score: typeof measurement.score === 'number' ? measurement.score : undefined,
    strengths: arrayOfStrings(asRecord(measurement.profile).strengths),
    needsWork: arrayOfStrings(asRecord(measurement.profile).weaknesses),
  }
}

function mapActivity(value: unknown): Activity {
  const activity = asRecord(value)
  return {
    id: stringValue(activity.id),
    title: stringValue(activity.title, '추천 활동'),
    category: stringValue(activity.fitnessElement, '활동 추천'),
    place: undefined,
    duration: undefined,
    icon: 'run',
    description: stringValue(activity.ageGroup, '아이와 함께 즐겨보세요.'),
    equipment: undefined,
    url: stringValue(activity.url),
  }
}

function mapCenter(value: unknown): Center {
  const center = asRecord(value)
  const distanceKm = typeof center.distanceKm === 'number' ? `${center.distanceKm.toFixed(1)}km` : '거리 정보 없음'
  return {
    id: stringValue(center.id),
    name: stringValue(center.name, '체력인증센터'),
    address: stringValue(center.address),
    distance: distanceKm,
    icon: 'tree',
    open: true,
    reservationUrl: stringValue(center.reservationUrl),
    stale: center.stale === true,
  }
}

function asRecord(value: unknown): Record<string, unknown> {
  return typeof value === 'object' && value !== null ? (value as Record<string, unknown>) : {}
}

function stringValue(value: unknown, fallback = '') {
  return typeof value === 'string' ? value : fallback
}

function arrayOfStrings(value: unknown) {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === 'string') : []
}
