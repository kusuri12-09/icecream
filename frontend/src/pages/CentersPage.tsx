import { useMemo, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { AppLayout, Card, SectionTitle } from '../components/AppLayout'
import { Icon } from '../components/Icon'
import { PillButton } from '../components/Button'
import { useCenters } from '../hooks/useFitnessData'

const PAGE_SIZE = 6

export function CentersPage() {
  const [sido, setSido] = useState('전체')
  const [query, setQuery] = useState('')
  const [location, setLocation] = useState<{ lat: number; lng: number } | null>(null)
  const [locationError, setLocationError] = useState('')
  const [page, setPage] = useState(1)
  const navigate = useNavigate()
  const { data: centers = [], isLoading, error } = useCenters(location ? { ...location, radiusKm: 10 } : {})
  const areas = useMemo(
    () => [
      '전체',
      ...Array.from(
        new Set(centers.map((center) => center.sido).filter((region): region is string => Boolean(region))),
      ).sort((left, right) => left.localeCompare(right, 'ko')),
    ],
    [centers],
  )
  const filtered = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()
    return centers.filter((center) => {
      const addressPrefix = center.address.trim().split(/\s+/).slice(0, 4).join(' ')
      const searchableText = `${center.name} ${center.sido ?? ''} ${center.region ?? ''} ${addressPrefix}`
      return (
        (location || sido === '전체' || center.sido === sido) &&
        (!normalizedQuery || searchableText.toLowerCase().includes(normalizedQuery))
      )
    })
  }, [centers, location, query, sido])
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const currentPage = Math.min(page, totalPages)
  const visibleCenters = filtered.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE)
  const pageNumbers = useMemo(() => {
    const firstPage = Math.max(1, Math.min(currentPage - 2, totalPages - 4))
    const lastPage = Math.min(totalPages, firstPage + 4)
    return Array.from({ length: lastPage - firstPage + 1 }, (_, index) => firstPage + index)
  }, [currentPage, totalPages])

  function requestLocation() {
    if (!navigator.geolocation) {
      setLocationError('이 브라우저에서는 현재 위치를 사용할 수 없어요.')
      return
    }
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({ lat: position.coords.latitude, lng: position.coords.longitude })
        setPage(1)
        setLocationError('')
      },
      () => setLocationError('현재 위치를 확인할 수 없어요. 지역 검색을 이용해주세요.'),
    )
  }

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
          aria-label="센터 검색"
          value={query}
          onChange={(event) => {
            setQuery(event.target.value)
            setPage(1)
          }}
          className="w-full bg-transparent text-sm outline-none"
          placeholder="지역이나 센터명을 검색해보세요"
        />
      </label>
      <div className="my-4 flex max-w-full gap-2 overflow-x-auto px-1 pb-1" aria-label="시도 선택">
        {areas.map((item) => (
          <PillButton
            key={item}
            active={!location && sido === item}
            onClick={() => {
              setLocation(null)
              setSido(item)
              setPage(1)
            }}
          >
            {item}
          </PillButton>
        ))}
      </div>
      <div className="relative h-44 overflow-hidden rounded-[2rem] bg-[#dfeee3]">
        <div className="absolute inset-0 opacity-70 [background:linear-gradient(28deg,transparent_0_28%,rgba(255,255,255,.8)_29%_32%,transparent_33%_61%,rgba(255,255,255,.75)_62%_65%,transparent_66%),repeating-linear-gradient(90deg,rgba(131,181,156,.16)_0_2px,transparent_2px_48px)]" />
        <Icon name="location_on" className="absolute left-[36%] top-[45%] z-10 text-3xl text-secondary" />
        <Icon name="location_on" className="absolute left-[64%] top-[28%] z-10 text-3xl text-secondary" />
        <button
          type="button"
          onClick={requestLocation}
          className="absolute right-3 top-3 flex items-center gap-1 rounded-full bg-white/85 px-3 py-2 text-xs text-primary"
        >
          <Icon name="my_location" className="text-base" />
          {location ? '현재 위치 적용됨' : '내 위치 기준'}
        </button>
      </div>
      {locationError && (
        <p role="alert" className="mt-3 rounded-2xl bg-error-container px-4 py-3 text-xs text-on-error-container">
          {locationError}
        </p>
      )}
      <section className="mt-7">
        <SectionTitle
          title="가까운 센터"
          action={<span className="text-xs text-on-surface-variant">{filtered.length}곳</span>}
        />
        <div className="mx-auto mt-3 grid w-full max-w-[420px] min-w-0 gap-2.5">
          {isLoading && <p className="py-8 text-center text-sm text-on-surface-variant">센터를 찾고 있어요…</p>}
          {error && (
            <p className="rounded-2xl bg-error-container px-4 py-3 text-sm text-on-error-container">
              센터를 불러오지 못했어요.
            </p>
          )}
          {!isLoading && !error && filtered.length === 0 && (
            <p className="py-8 text-center text-sm text-on-surface-variant">조건에 맞는 센터가 없어요.</p>
          )}
          {visibleCenters.map((center) => (
            <Card
              key={center.id}
              className="mx-auto flex min-h-[102px] w-full min-w-0 max-w-full items-center gap-2 overflow-hidden p-2.5 shadow-soft"
            >
              <div className="grid size-16 flex-none place-items-center rounded-2xl bg-gradient-to-br from-[#e0f1e3] to-[#f6dfc9] text-3xl">
                <Icon name={center.icon} className="text-3xl text-primary" />
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
                type="button"
                className="shrink-0 rounded-full bg-primary-container px-2.5 py-2 text-[11px] font-semibold text-primary"
                onClick={() => navigate(`/centers/nearby?centerId=${encodeURIComponent(center.id)}`)}
              >
                상세보기
              </button>
            </Card>
          ))}
        </div>
        {!isLoading && !error && filtered.length > 0 && totalPages > 1 && (
          <nav className="mt-5 flex items-center justify-center gap-1" aria-label="센터 목록 페이지">
            <button
              type="button"
              aria-label="이전 페이지"
              disabled={currentPage === 1}
              onClick={() => setPage((value) => Math.max(1, value - 1))}
              className="grid size-10 place-items-center rounded-full text-on-surface-variant transition hover:bg-surface-container-low disabled:cursor-not-allowed disabled:opacity-40"
            >
              <Icon name="chevron_left" />
            </button>
            {pageNumbers.map((pageNumber) => (
              <button
                key={pageNumber}
                type="button"
                aria-label={`${pageNumber}페이지`}
                aria-current={currentPage === pageNumber ? 'page' : undefined}
                onClick={() => setPage(pageNumber)}
                className={`grid size-10 place-items-center rounded-full text-sm transition ${
                  currentPage === pageNumber
                    ? 'bg-primary text-white'
                    : 'text-on-surface-variant hover:bg-surface-container-low'
                }`}
              >
                {pageNumber}
              </button>
            ))}
            <button
              type="button"
              aria-label="다음 페이지"
              disabled={currentPage === totalPages}
              onClick={() => setPage((value) => Math.min(totalPages, value + 1))}
              className="grid size-10 place-items-center rounded-full text-on-surface-variant transition hover:bg-surface-container-low disabled:cursor-not-allowed disabled:opacity-40"
            >
              <Icon name="chevron_right" />
            </button>
          </nav>
        )}
      </section>
    </AppLayout>
  )
}

export function NearbyCenterPage() {
  const [searchParams] = useSearchParams()
  const centerId = searchParams.get('centerId')
  const { data: centers = [], isLoading } = useCenters()
  const center = centers.find((item) => item.id === centerId) ?? centers[0]

  if (isLoading || !center) {
    return (
      <AppLayout active="centers" back className="!p-0">
        <div className="grid min-h-dvh place-items-center text-sm text-on-surface-variant">
          센터 정보를 불러오고 있어요…
        </div>
      </AppLayout>
    )
  }

  return (
    <AppLayout active="centers" back className="!p-0">
      <div className="relative h-[46vh] min-h-[370px] bg-[#dfeee3]">
        <div className="absolute inset-0 opacity-70 [background:linear-gradient(28deg,transparent_0_28%,rgba(255,255,255,.8)_29%_32%,transparent_33%_61%,rgba(255,255,255,.75)_62%_65%,transparent_66%),repeating-linear-gradient(90deg,rgba(131,181,156,.16)_0_2px,transparent_2px_48px)]" />
        <Icon name="location_on" className="absolute left-[36%] top-[45%] text-3xl text-secondary" />
        <Icon name="location_on" className="absolute left-[64%] top-[28%] text-3xl text-secondary" />
      </div>
      <section className="relative -mt-7 rounded-t-[2rem] bg-background px-6 pb-9 pt-6">
        <span className="mx-auto mb-5 block h-1 w-11 rounded-full bg-outline-variant" />
        <span className="font-label text-sm font-semibold text-on-surface-variant">가장 가까운 센터</span>
        <h1 className="mt-3 font-display text-[25px] font-bold leading-tight tracking-[-.07em]">{center.name}</h1>
        <p className="mt-3 flex items-center gap-1 text-sm text-on-surface-variant">
          <Icon name="location_on" />
          {center.address}
        </p>
        <div className="my-5 flex gap-2">
          <span className="rounded-xl bg-white px-2.5 py-2 text-[10px] text-on-surface-variant">
            <Icon name="near_me" className="text-sm text-primary" /> {center.distance}
          </span>
          <span className="rounded-xl bg-white px-2.5 py-2 text-[10px] text-on-surface-variant">
            <Icon name="child_care" className="text-sm text-primary" /> 유아 측정
          </span>
          {center.stale && (
            <span className="rounded-xl bg-tertiary-container px-2.5 py-2 text-[10px] text-[#625f4e]">캐시 데이터</span>
          )}
        </div>
        {center.reservationUrl ? (
          <a
            href={center.reservationUrl}
            target="_blank"
            rel="noreferrer"
            className="flex min-h-12 items-center justify-center gap-2 rounded-full bg-primary px-6 font-semibold text-white"
          >
            예약 페이지 열기 <Icon name="open_in_new" />
          </a>
        ) : (
          <p className="rounded-2xl bg-surface-container-low px-4 py-3 text-center text-sm text-on-surface-variant">
            예약 링크가 등록되지 않은 센터예요.
          </p>
        )}
        <p className="mt-5 flex gap-2 text-xs leading-5 text-on-surface-variant">
          <Icon name="info" className="text-primary" />
          국민체력100 유아기 측정은 참고용으로 진행돼요.
        </p>
      </section>
    </AppLayout>
  )
}
