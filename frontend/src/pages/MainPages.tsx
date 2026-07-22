import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ApiError } from '../api/client'
import { AppLayout, Card, GradeBadge, SectionTitle } from '../components/AppLayout'
import { Character } from '../components/Character'
import { EmptyState, ErrorState, LoadingState } from '../components/AsyncState'
import { Icon } from '../components/Icon'
import { PrimaryButton } from '../components/Button'
import {
  useActivities,
  useChild,
  useMeasurement,
  useRecords,
  useRegionalInsight,
  useRegionalMap,
  useSaveChild,
} from '../hooks/useFitnessData'
import type { ChildProfile, MeasurementRecord } from '../types/models'

export function OnboardingPage() {
  const { data: child, isLoading } = useChild()
  if (isLoading) {
    return (
      <AppLayout className="pb-10">
        <div className="grid min-h-[50vh] place-items-center text-sm text-on-surface-variant" role="status">
          프로필을 준비하고 있어요…
        </div>
      </AppLayout>
    )
  }
  return <OnboardingForm key={child?.id ?? 'new'} child={child ?? null} />
}

function OnboardingForm({ child }: { child: ChildProfile | null }) {
  const navigate = useNavigate()
  const saveChild = useSaveChild()
  const [nickname, setNickname] = useState(child?.name ?? '')
  const [gender, setGender] = useState<'male' | 'female'>(child?.gender ?? 'male')
  const [birthYearMonth, setBirthYearMonth] = useState(child?.birthYearMonth ?? '')
  const [error, setError] = useState('')

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const trimmedNickname = nickname.trim()
    setError('')
    if (!trimmedNickname) {
      setError('아이 이름을 입력해주세요.')
      return
    }
    if (!/^\d{4}-(0[1-9]|1[0-2])$/.test(birthYearMonth)) {
      setError('생년월을 올바르게 선택해주세요.')
      return
    }

    try {
      await saveChild.mutateAsync({
        childId: child?.id,
        nickname: trimmedNickname,
        gender: gender === 'female' ? 'FEMALE' : 'MALE',
        birthYearMonth,
      })
      navigate('/dashboard', { replace: true })
    } catch (cause) {
      if (cause instanceof ApiError && cause.status === 401) {
        navigate('/login', { replace: true })
        return
      }
      setError(cause instanceof ApiError ? cause.message : '프로필을 저장하지 못했습니다. 잠시 후 다시 시도해주세요.')
    }
  }

  return (
    <AppLayout className="pb-10">
      <section className="px-2 pb-7 text-center">
        <div
          role="img"
          aria-label="프로필 일러스트 영역"
          className="mx-auto mb-6 size-40 rounded-full bg-[radial-gradient(circle_at_30%_30%,#fff_0_28%,#e1f6ec_29%_53%,#b5ead7_54%_55%,#faf9f5_56%)]"
        />
        <span className="font-label text-sm font-semibold text-on-surface-variant">우리 아이의 건강한 성장 기록</span>
        <h1 className="mt-2 font-display text-[28px] font-bold leading-tight tracking-[-.08em]">
          아이의 성장을
          <br />
          함께 기록해요
        </h1>
        <p className="mt-3 text-base leading-7 text-on-surface-variant">
          국가 표준 체력 기준으로 우리 아이의
          <br />
          체력 성장을 부드럽게 확인해보세요.
        </p>
      </section>
      <Card className="p-5">
        <div className="mb-5 flex items-center gap-3">
          <span className="grid size-9 place-items-center rounded-xl bg-primary-container text-primary">
            <Icon name="face" />
          </span>
          <div>
            <p className="font-label text-xs font-semibold text-on-surface-variant">
              {child ? '프로필을 수정해요' : '처음이시라면'}
            </p>
            <h2 className="font-display text-lg font-bold tracking-[-.06em]">아이 프로필을 등록해요</h2>
          </div>
        </div>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <label className="block">
            <span className="mb-2 block font-label text-xs font-semibold text-on-surface-variant">아이 이름</span>
            <input
              name="nickname"
              value={nickname}
              onChange={(event) => setNickname(event.target.value)}
              aria-invalid={Boolean(error && !nickname.trim())}
              aria-describedby={error ? 'profile-error' : undefined}
              className="h-[52px] w-full rounded-full border border-outline-variant/50 bg-[#fffdf5] px-5 outline-none focus:border-primary focus:ring-4 focus:ring-primary-container/50"
              placeholder="아이 이름을 입력해주세요"
            />
          </label>
          <div>
            <span className="mb-2 block font-label text-xs font-semibold text-on-surface-variant">성별</span>
            <div className="flex gap-1 rounded-full bg-surface-container-low p-1">
              <button
                type="button"
                aria-pressed={gender === 'male'}
                onClick={() => setGender('male')}
                className={`flex h-11 flex-1 items-center justify-center gap-1 rounded-full font-label text-sm ${gender === 'male' ? 'bg-white text-primary shadow-sm' : 'text-on-surface-variant'}`}
              >
                <Icon name="boy" />
                남아
              </button>
              <button
                type="button"
                aria-pressed={gender === 'female'}
                onClick={() => setGender('female')}
                className={`flex h-11 flex-1 items-center justify-center gap-1 rounded-full font-label text-sm ${gender === 'female' ? 'bg-white text-primary shadow-sm' : 'text-on-surface-variant'}`}
              >
                <Icon name="girl" />
                여아
              </button>
            </div>
          </div>
          <label className="block">
            <span className="mb-2 block font-label text-xs font-semibold text-on-surface-variant">생년월</span>
            <input
              type="text"
              name="birthYearMonth"
              value={birthYearMonth}
              inputMode="numeric"
              maxLength={7}
              placeholder="YYYY-MM"
              aria-invalid={Boolean(error && !birthYearMonth)}
              aria-describedby={error ? 'profile-error' : undefined}
              onChange={(event) => {
                const digits = event.target.value.replace(/\D/g, '').slice(0, 6)
                setBirthYearMonth(digits.length > 4 ? `${digits.slice(0, 4)}-${digits.slice(4)}` : digits)
              }}
              className="h-[52px] w-full rounded-full border border-outline-variant/50 bg-[#fffdf5] px-5 outline-none focus:border-primary"
            />
          </label>
          {error && (
            <p
              id="profile-error"
              role="alert"
              className="rounded-2xl bg-error-container px-4 py-3 text-sm text-on-error-container"
            >
              {error}
            </p>
          )}
          <PrimaryButton type="submit" className="mt-2 w-full" disabled={saveChild.isPending}>
            {saveChild.isPending ? '저장하고 있어요…' : child ? '프로필 저장하기' : '성장 기록 시작하기'}
          </PrimaryButton>
        </form>
      </Card>
    </AppLayout>
  )
}
export function HomePage() {
  const navigate = useNavigate()
  const childQuery = useChild()
  const recordsQuery = useRecords()
  const activitiesQuery = useActivities()
  const child = childQuery.data
  const records = recordsQuery.data ?? []
  const activities = activitiesQuery.data ?? []
  const latestRecord = records[0]

  if (childQuery.isLoading || recordsQuery.isLoading || activitiesQuery.isLoading) {
    return (
      <AppLayout active="home">
        <LoadingState message="성장 데이터를 불러오고 있어요…" />
      </AppLayout>
    )
  }
  if (childQuery.error || recordsQuery.error || activitiesQuery.error) {
    return (
      <AppLayout active="home">
        <ErrorState
          message="성장 데이터를 불러오지 못했어요."
          onRetry={() => {
            void childQuery.refetch()
            void recordsQuery.refetch()
            void activitiesQuery.refetch()
          }}
        />
      </AppLayout>
    )
  }
  if (!child) {
    return (
      <AppLayout active="home">
        <EmptyState
          message="먼저 아이 프로필을 등록해주세요."
          action={
            <button
              type="button"
              onClick={() => navigate('/onboarding')}
              className="rounded-full bg-primary px-5 py-3 font-semibold text-white"
            >
              프로필 등록하기
            </button>
          }
        />
      </AppLayout>
    )
  }

  return (
    <AppLayout active="home">
      <section className="px-1">
        <h1 className="font-display text-[22px] tracking-[-.07em]">{child.name}님, 오늘도 쑥쑥 자라요!</h1>
        <p className="mt-1 text-sm text-on-surface-variant">아이의 작은 변화도 소중한 성장 기록이에요.</p>
      </section>
      <Card className="mt-5 flex min-h-48 items-center justify-between overflow-hidden bg-gradient-to-br from-white to-[#f5faf7] p-7">
        <div>
          <span className="font-label text-sm text-on-surface-variant">현재 성장 등급</span>
          {latestRecord ? (
            <>
              <h2 className="mt-3 flex items-center gap-2 font-display text-[22px] text-primary">
                <span className="grid size-10 place-items-center rounded-full bg-primary-container">
                  <Icon name="seedling" />
                </span>
                {latestRecord.grade} 등급
              </h2>
              <p className="mt-3 leading-7 text-on-surface-variant">{latestRecord.date} 측정 기록이에요.</p>
            </>
          ) : (
            <p className="mt-3 leading-7 text-on-surface-variant">아직 측정 기록이 없어요.</p>
          )}
        </div>
        <Character />
      </Card>
      <section className="mt-8">
        <SectionTitle
          title="최근 측정 기록"
          action={
            <button
              type="button"
              className="font-display text-sm font-bold text-primary"
              onClick={() => navigate('/records')}
            >
              전체보기
            </button>
          }
        />
        {records.length ? (
          <div className="mt-4 grid grid-cols-2 gap-4">
            {records.slice(0, 2).map((record, index) => (
              <RecordTile
                key={record.id}
                record={record}
                tone={index === 0 ? 'coral' : 'mint'}
                onClick={() => navigate(`/records/${record.id}`)}
              />
            ))}
          </div>
        ) : (
          <EmptyState
            message="아직 측정 기록이 없어요."
            action={
              <button
                type="button"
                onClick={() => navigate('/diagnosis/input')}
                className="rounded-full bg-primary px-4 py-2 font-semibold text-white"
              >
                첫 측정 시작하기
              </button>
            }
          />
        )}
      </section>
      <section className="mt-8">
        <h2 className="mb-4 font-display text-[21px] tracking-[-.07em]">오늘의 성장 팁</h2>
        {activities[0] ? (
          <Card className="border-[#ebe4ce] bg-[#f7f3e7] p-7">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-white px-4 py-2 text-sm text-on-surface-variant">
              <Icon name="lightbulb" />
              {activities[0].category}
            </span>
            <h3 className="mt-5 font-display text-xl tracking-[-.07em]">{activities[0].title}</h3>
            <p className="mt-3 leading-8 text-on-surface-variant">{activities[0].description}</p>
            <PrimaryButton className="mt-1" onClick={() => navigate('/activities')}>
              자세히 알아보기
            </PrimaryButton>
            <div className="mt-6 grid h-28 place-items-center rounded-3xl bg-gradient-to-br from-[#dcefdc] to-[#f5dfc7]">
              <span aria-hidden="true" className="size-16 rounded-[38%] bg-white/25" />
            </div>
          </Card>
        ) : (
          <EmptyState message="추천 활동을 불러오지 못했어요." />
        )}
      </section>
      <div className="mt-9 grid grid-cols-4 gap-2">
        {[
          ['fitness_center', '운동하기', '/activities'],
          ['nutrition', '식단 가이드', ''],
          ['history', '성장 리포트', '/growth'],
          ['chat', '전문가 상담', ''],
        ].map(([icon, label, path]) => (
          <button
            key={label}
            type="button"
            className={`flex flex-col items-center gap-2 text-xs ${path ? '' : 'cursor-not-allowed opacity-60'}`}
            onClick={path ? () => navigate(path) : undefined}
            aria-disabled={!path}
            title={path ? undefined : '준비 중인 기능이에요'}
          >
            <span className="grid size-14 place-items-center rounded-2xl border border-outline-variant/40 bg-white shadow-soft">
              <Icon name={icon} />
            </span>
            {label}
          </button>
        ))}
      </div>
      <button
        type="button"
        className="fixed bottom-24 right-[max(24px,calc(50%_-_220px))] z-20 grid size-14 place-items-center rounded-full bg-primary text-white shadow-lg"
        onClick={() => navigate('/diagnosis/input')}
      >
        <Icon name="add_task" />
      </button>
    </AppLayout>
  )
}

function RecordTile({
  record,
  tone,
  onClick,
}: {
  record: MeasurementRecord
  tone: 'mint' | 'coral'
  onClick: () => void
}) {
  return (
    <button
      type="button"
      className="min-h-48 rounded-3xl border border-outline-variant/40 bg-white p-5 text-left shadow-soft"
      onClick={onClick}
    >
      <span
        className={`mb-5 grid size-12 place-items-center rounded-full ${tone === 'mint' ? 'bg-[#e1f7ef] text-primary' : 'bg-[#ffe1df] text-secondary'}`}
      >
        <Icon name="analytics" />
      </span>
      <h3 className="font-display text-base font-medium tracking-[-.06em]">{record.date}</h3>
      <p className="mt-2 text-sm">{record.grade} 등급</p>
      <span className="mt-4 block text-sm leading-6 text-primary">
        {record.type === 'official' ? '정식 측정' : '자가측정'}
      </span>
    </button>
  )
}

export function DashboardPage() {
  const navigate = useNavigate()
  const childQuery = useChild()
  const recordsQuery = useRecords()
  const latestRecord = recordsQuery.data?.[0]
  const latestMeasurementQuery = useMeasurement(latestRecord?.id)
  const child = childQuery.data

  if (childQuery.isLoading || recordsQuery.isLoading || latestMeasurementQuery.isLoading)
    return (
      <AppLayout active="home">
        <LoadingState message="대시보드를 준비하고 있어요…" />
      </AppLayout>
    )
  if (childQuery.error || recordsQuery.error || latestMeasurementQuery.error)
    return (
      <AppLayout active="home">
        <ErrorState
          message="대시보드 데이터를 불러오지 못했어요."
          onRetry={() => {
            void childQuery.refetch()
            void recordsQuery.refetch()
          }}
        />
      </AppLayout>
    )
  if (!child)
    return (
      <AppLayout active="home">
        <EmptyState
          message="먼저 아이 프로필을 등록해주세요."
          action={
            <button
              type="button"
              onClick={() => navigate('/onboarding')}
              className="rounded-full bg-primary px-5 py-3 font-semibold text-white"
            >
              프로필 등록하기
            </button>
          }
        />
      </AppLayout>
    )
  return (
    <AppLayout active="home">
      <section className="pt-2 text-center">
        <div className="mx-auto w-fit">
          <Character large />
        </div>
        <div className="-mt-1">
          {latestRecord ? (
            <GradeBadge grade={latestRecord.grade} />
          ) : (
            <span className="inline-flex rounded-full bg-surface-container-low px-4 py-2 text-sm text-on-surface-variant">
              아직 진단 전
            </span>
          )}
          <h1 className="mt-2 font-display text-[28px] font-bold tracking-[-.09em]">{child.name}의 성장 일기</h1>
          <p className="mt-2 text-base text-on-surface-variant">건강하게 쑥쑥 자라나고 있어요!</p>
        </div>
      </section>
      <Card className="mt-9 border-l-4 border-l-primary p-7">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="font-display text-2xl font-bold tracking-[-.08em]">최근 진단 기록</h2>
            {latestRecord ? (
              <p className="mt-2 text-[17px] text-on-surface-variant">{latestRecord.date} 측정</p>
            ) : (
              <p className="mt-2 text-[17px] text-on-surface-variant">아직 측정 기록이 없어요.</p>
            )}
          </div>
          <Icon name="analytics" className="text-primary" />
        </div>
        {latestMeasurementQuery.data ? (
          <div className="mt-5 flex flex-wrap gap-2">
            {latestMeasurementQuery.data.profile.strengths.map((strength) => (
              <span
                key={`strength-${strength}`}
                className="inline-flex items-center gap-1 rounded-full bg-primary-container px-4 py-2 text-sm text-primary"
              >
                <Icon name="trending_up" className="text-base" />
                {strength}
              </span>
            ))}
            {latestMeasurementQuery.data.profile.weaknesses.map((weakness) => (
              <span
                key={`weakness-${weakness}`}
                className="inline-flex items-center gap-1 rounded-full bg-[#ffd9d5] px-4 py-2 text-sm text-secondary"
              >
                <Icon name="fitness_center" className="text-base" />
                {weakness} 개선 필요
              </span>
            ))}
            {!latestMeasurementQuery.data.profile.strengths.length &&
              !latestMeasurementQuery.data.profile.weaknesses.length && (
                <span className="text-sm text-on-surface-variant">프로필을 분석할 데이터가 부족해요.</span>
              )}
          </div>
        ) : (
          <button
            type="button"
            onClick={() => navigate('/diagnosis/input')}
            className="mt-5 rounded-full bg-primary-container px-4 py-2 text-sm font-semibold text-primary"
          >
            첫 측정 시작하기
          </button>
        )}
      </Card>
      <div className="mt-7 grid gap-3.5">
        <DashboardAction icon="fitness_center" text="체력 진단하기" onClick={() => navigate('/diagnosis')} />
        <DashboardAction icon="location_on" text="근처 센터 찾기" tone="cream" onClick={() => navigate('/centers')} />
        <DashboardAction icon="groups" text="우리 동네 참여 현황" tone="white" onClick={() => navigate('/regional')} />
      </div>
    </AppLayout>
  )
}

function DashboardAction({
  icon,
  text,
  tone = 'mint',
  onClick,
}: {
  icon: string
  text: string
  tone?: 'mint' | 'cream' | 'white'
  onClick: () => void
}) {
  return (
    <button
      onClick={onClick}
      className={`flex min-h-[70px] items-center gap-4 rounded-full px-6 text-[17px] ${tone === 'mint' ? 'bg-primary-container text-primary' : tone === 'cream' ? 'bg-tertiary-container text-[#625f4e]' : 'bg-white text-on-surface shadow-soft'}`}
    >
      <Icon name={icon} />
      <span className="flex-1 text-left">{text}</span>
      <Icon name="chevron_right" />
    </button>
  )
}

export function RegionalPage() {
  const insightQuery = useRegionalInsight()
  const regionalMapQuery = useRegionalMap()
  const insight = insightQuery.data
  const regionalMap = regionalMapQuery.data ?? []
  if (insightQuery.isLoading || regionalMapQuery.isLoading)
    return (
      <AppLayout active="centers">
        <LoadingState message="지역 참여 데이터를 불러오고 있어요…" />
      </AppLayout>
    )
  if (insightQuery.error || regionalMapQuery.error)
    return (
      <AppLayout active="centers">
        <ErrorState
          message="지역 참여 데이터를 불러오지 못했어요."
          onRetry={() => {
            void insightQuery.refetch()
            void regionalMapQuery.refetch()
          }}
        />
      </AppLayout>
    )
  const bars = regionalMap
    .slice(0, 5)
    .map((region) => [region.sidoSigungu, Math.round(region.participationRate * 100)] as const)
  const regionName = insight?.region ?? regionalMap[0]?.sidoSigungu ?? '전국'
  const relativeMessage =
    insight?.relativeLevel === 'ABOVE_AVG'
      ? '참여가 활발해요!'
      : insight?.relativeLevel === 'BELOW_AVG'
        ? '참여를 시작해보세요.'
        : '전국 평균과 비슷해요.'
  return (
    <AppLayout active="centers">
      <PageHeading
        eyebrow="우리 동네 데이터"
        title={`${regionName} 참여율 랭킹`}
        description={
          <>
            아이들이 건강하게 자라는 동네,
            <br />
            우리 지역의 참여 현황을 확인해요.
          </>
        }
      />
      <Card className="flex items-center gap-4 border-0 bg-primary-container p-5">
        <div className="grid size-24 flex-none place-items-center rounded-full border-4 border-white bg-[#d9f6e9] text-5xl">
          <Icon name="location_on" />
        </div>
        <div>
          <span className="rounded-full bg-white/70 px-3 py-1.5 text-xs font-semibold text-primary">
            {insight?.region ?? '우리 지역'} 참여 현황
          </span>
          <h2 className="mt-3 font-display text-xl font-bold leading-tight text-primary">
            우리 동네는
            <br />
            <strong>{relativeMessage}</strong>
          </h2>
          <p className="mt-2 text-xs leading-5 text-primary">
            {insight?.message ?? '지역 측정 데이터를 확인해보세요.'}
          </p>
        </div>
      </Card>
      <Card className="mt-5 p-5">
        <SectionTitle
          title="지역별 참여율"
          action={
            <span className="rounded-full bg-surface-container-low px-3 py-2 text-xs text-on-surface-variant">
              {regionName}
            </span>
          }
        />
        <div className="mt-6 grid gap-4">
          {bars.map(([name, value], index) => (
            <div className="grid grid-cols-[20px_52px_1fr_38px] items-center gap-2 text-xs" key={name}>
              <b className="text-center text-primary">{index + 1}</b>
              <span>{name}</span>
              <div className="h-2 overflow-hidden rounded-full bg-surface-container">
                <i className="block h-full rounded-full bg-primary" style={{ width: `${value}%` }} />
              </div>
              <strong className="text-right text-primary">{value}%</strong>
            </div>
          ))}
        </div>
      </Card>
      <Card className="mt-5 p-5">
        <SectionTitle title="지역별 관심도 분포" action={<Icon name="map" className="text-primary" />} />
        <div className="mt-4 grid gap-3">
          {regionalMap.slice(0, 5).map((region) => (
            <div key={region.sidoSigungu} className="grid grid-cols-[1fr_52px] items-center gap-3 text-xs">
              <div>
                <div className="mb-1 flex justify-between gap-3">
                  <span>{region.sidoSigungu}</span>
                  <span className="text-on-surface-variant">{region.measureCount.toLocaleString()}건</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-surface-container">
                  <i
                    className="block h-full rounded-full bg-primary"
                    style={{ width: `${Math.round(region.participationRate * 100)}%` }}
                  />
                </div>
              </div>
              <strong className="text-right text-primary">{Math.round(region.participationRate * 100)}%</strong>
            </div>
          ))}
        </div>
      </Card>
    </AppLayout>
  )
}

function PageHeading({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string
  title: string
  description: React.ReactNode
}) {
  return (
    <section className="px-2 pb-6">
      <span className="font-label text-sm font-semibold text-on-surface-variant">{eyebrow}</span>
      <h1 className="mt-2 font-display text-[28px] font-bold leading-tight tracking-[-.09em]">{title}</h1>
      <p className="mt-3 text-base leading-7 text-on-surface-variant">{description}</p>
    </section>
  )
}
