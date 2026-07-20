import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AppLayout, Card, SectionTitle } from '../components/AppLayout'
import { Icon } from '../components/Icon'
import { PillButton, PrimaryButton } from '../components/Button'
import { useCenters } from '../hooks/useFitnessData'

export function CentersPage() {
  const { data: centers = [] } = useCenters()
  const [area, setArea] = useState('전체')
  const [query, setQuery] = useState('')
  const navigate = useNavigate()
  const filtered = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()
    return centers.filter(
      (center) =>
        (area === '전체' || center.address.includes(area)) &&
        (!normalizedQuery || `${center.name} ${center.address}`.toLowerCase().includes(normalizedQuery)),
    )
  }, [centers, area, query])
  return (
    <AppLayout active="centers">
      <section className="px-2 pb-4">
        <span className="font-label text-sm font-semibold text-on-surface-variant">국민체력100</span>
        <h1 className="mt-2 font-display text-[28px] leading-tight tracking-[-.09em]">체력인증센터 찾기</h1>
        <p className="mt-3 text-base leading-7 text-on-surface-variant">
          우리 아이와 가까운 센터에서
          <br />
          무료 정식 측정을 받아보세요.
        </p>
      </section>
      <label className="flex h-[52px] items-center gap-2 rounded-full border border-outline-variant/50 bg-white px-4">
        <Icon name="search" className="text-on-surface-variant" />
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="w-full bg-transparent text-sm outline-none"
          placeholder="지역이나 센터명을 검색해보세요"
        />
      </label>
      <div className="my-4 flex gap-2 overflow-x-auto">
        {['전체', '강남구', '서초구', '송파구'].map((item) => (
          <PillButton key={item} active={area === item} onClick={() => setArea(item)}>
            {item}
          </PillButton>
        ))}
      </div>
      <div className="relative h-44 overflow-hidden rounded-[2rem] bg-[#dfeee3]">
        <div className="absolute inset-0 opacity-70 [background:linear-gradient(28deg,transparent_0_28%,rgba(255,255,255,.8)_29%_32%,transparent_33%_61%,rgba(255,255,255,.75)_62%_65%,transparent_66%),repeating-linear-gradient(90deg,rgba(131,181,156,.16)_0_2px,transparent_2px_48px)]" />
        <Icon name="location_on" className="absolute left-[36%] top-[45%] z-10 text-3xl text-secondary" />
        <Icon name="location_on" className="absolute left-[64%] top-[28%] z-10 text-3xl text-secondary" />
        <span className="absolute right-3 top-3 flex items-center gap-1 rounded-full bg-white/85 px-3 py-2 text-xs text-primary">
          <Icon name="my_location" className="text-base" />내 위치 기준
        </span>
      </div>
      <section className="mt-7">
        <SectionTitle
          title="가까운 센터"
          action={<span className="text-xs text-on-surface-variant">{filtered.length}곳</span>}
        />
        <div className="mt-3 grid gap-2.5">
          {filtered.map((center) => (
            <Card key={center.id} className="flex min-h-[102px] items-center gap-3 p-2.5 shadow-soft">
              <div className="grid size-[76px] flex-none place-items-center rounded-2xl bg-gradient-to-br from-[#e0f1e3] to-[#f6dfc9] text-4xl">
                <Icon name={center.icon} className="text-4xl text-primary" />
              </div>
              <div className="min-w-0 flex-1">
                <h3 className="truncate text-sm font-bold tracking-[-.06em]">{center.name}</h3>
                <p className="mt-1 truncate text-[10px] text-on-surface-variant">{center.address}</p>
                <span className="mt-2 inline-flex items-center gap-1 text-[11px] text-primary">
                  <Icon name="near_me" className="text-sm" />
                  {center.distance}
                </span>
              </div>
              <button
                className="rounded-full bg-primary-container px-3 py-2 text-[11px] font-semibold text-primary"
                onClick={() => navigate('/centers/nearby')}
              >
                상세보기
              </button>
            </Card>
          ))}
        </div>
      </section>
    </AppLayout>
  )
}

export function NearbyCenterPage() {
  return (
    <AppLayout active="centers" back className="!p-0">
      <div className="relative h-[46vh] min-h-[370px] bg-[#dfeee3]">
        <div className="absolute inset-0 opacity-70 [background:linear-gradient(28deg,transparent_0_28%,rgba(255,255,255,.8)_29%_32%,transparent_33%_61%,rgba(255,255,255,.75)_62%_65%,transparent_66%),repeating-linear-gradient(90deg,rgba(131,181,156,.16)_0_2px,transparent_2px_48px)]" />
        <Icon name="location_on" className="absolute left-[36%] top-[45%] text-3xl text-secondary" />
        <Icon name="location_on" className="absolute left-[64%] top-[28%] text-3xl text-secondary" />
        <button
          aria-label="내 위치로 이동"
          className="absolute bottom-5 right-5 grid size-12 place-items-center rounded-full bg-white text-primary shadow-soft"
        >
          <Icon name="my_location" />
        </button>
      </div>
      <section className="relative -mt-7 rounded-t-[2rem] bg-background px-6 pb-9 pt-6">
        <span className="mx-auto mb-5 block h-1 w-11 rounded-full bg-outline-variant" />
        <span className="font-label text-sm font-semibold text-on-surface-variant">가장 가까운 센터</span>
        <h1 className="mt-3 font-display text-[25px] font-bold leading-tight tracking-[-.07em]">
          아이그로우 피트니스
          <br />
          삼성점
        </h1>
        <p className="mt-3 flex items-center gap-1 text-sm text-on-surface-variant">
          <Icon name="location_on" />
          서울 강남구 테헤란로 00
        </p>
        <div className="my-5 flex gap-2">
          <span className="rounded-xl bg-white px-2.5 py-2 text-[10px] text-on-surface-variant">
            <Icon name="near_me" className="text-sm text-primary" /> 1.2km
          </span>
          <span className="rounded-xl bg-white px-2.5 py-2 text-[10px] text-on-surface-variant">
            <Icon name="schedule" className="text-sm text-primary" /> 운영중
          </span>
          <span className="rounded-xl bg-white px-2.5 py-2 text-[10px] text-on-surface-variant">
            <Icon name="child_care" className="text-sm text-primary" /> 유아 측정
          </span>
        </div>
        <div className="flex gap-2">
          <PrimaryButton className="flex-1" onClick={() => undefined} trailingIcon="open_in_new">
            예약 페이지 열기
          </PrimaryButton>
          <button className="grid size-12 place-items-center rounded-full bg-primary-container text-primary">
            <Icon name="call" />
          </button>
        </div>
        <p className="mt-5 flex gap-2 text-xs leading-5 text-on-surface-variant">
          <Icon name="info" className="text-primary" />
          국민체력100 유아기 측정은 참고용으로 진행돼요.
        </p>
      </section>
    </AppLayout>
  )
}
