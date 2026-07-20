import type { Activity, Center, ChildProfile, MeasurementRecord } from '../types/models'

const child: ChildProfile = {
  id: 'jiwoo',
  name: '지우',
  ageLabel: '만 5세 · 61개월',
  gender: 'male',
  avatarIcon: 'user_smile',
}

const records: MeasurementRecord[] = [
  {
    id: 'r-1',
    date: '2023년 10월 24일',
    type: 'official',
    grade: '새싹',
    score: 72,
    strengths: ['순발력', '유연성'],
    needsWork: ['근력'],
  },
  {
    id: 'r-2',
    date: '2023년 07월 18일',
    type: 'official',
    grade: '씨앗',
    score: 58,
    strengths: ['유연성'],
    needsWork: ['근력', '지구력'],
  },
  {
    id: 'r-3',
    date: '2023년 04월 03일',
    type: 'self',
    grade: '씨앗',
    score: 49,
    strengths: ['균형감'],
    needsWork: ['순발력'],
  },
]

const activities: Activity[] = [
  {
    id: 'a-1',
    title: '엉금엉금 거북이 놀이',
    category: '민첩성',
    place: '실내',
    duration: '10분',
    icon: 'run',
    description: '낮은 자세로 움직이며 몸의 방향을 바꿔봐요.',
    equipment: false,
  },
  {
    id: 'a-2',
    title: '징검다리 톡톡',
    category: '순발력',
    place: '실내',
    duration: '15분',
    icon: 'footprint',
    description: '바닥에 놓은 쿠션을 차례로 건너가요.',
    equipment: true,
  },
  {
    id: 'a-3',
    title: '높이높이 점프팡',
    category: '근력',
    place: '야외',
    duration: '20분',
    icon: 'run',
    description: '부모님과 함께 안전하게 점프해요.',
    equipment: false,
  },
]

const centers: Center[] = [
  {
    id: 'c-1',
    name: '꿈나무 성장센터',
    address: '서울시 송파구 올림픽로 00',
    distance: '1.2km',
    icon: 'tree',
    open: true,
  },
  {
    id: 'c-2',
    name: '아이핏 피트니스',
    address: '서울시 강남구 테헤란로 00',
    distance: '2.8km',
    icon: 'home_4',
    open: true,
  },
  {
    id: 'c-3',
    name: '키즈 요가 스튜디오',
    address: '서울시 서초구 반포대로 00',
    distance: '4.1km',
    icon: 'community',
    open: false,
  },
]

const delay = <T>(value: T) => new Promise<T>((resolve) => window.setTimeout(() => resolve(value), 180))
export const getChild = () => delay(child)
export const getRecords = () => delay(records)
export const getActivities = () => delay(activities)
export const getCenters = () => delay(centers)
