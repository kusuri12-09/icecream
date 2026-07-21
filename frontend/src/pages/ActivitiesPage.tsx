import { useState } from 'react'
import { AppLayout, Card, SectionTitle } from '../components/AppLayout'
import { Icon } from '../components/Icon'
import { PillButton } from '../components/Button'
import { useActivities } from '../hooks/useFitnessData'

const fitnessFilters = [
  ['', '전체'],
  ['CARDIO', '심폐지구력'],
  ['GRIP', '근력'],
  ['MUSCULAR_END', '근지구력'],
  ['FLEXIBILITY', '유연성'],
  ['AGILITY', '민첩성'],
  ['POWER', '순발력'],
  ['COORDINATION', '협응력'],
] as const

export function ActivitiesPage() {
  const [filter, setFilter] = useState('')
  const { data: activities = [], isLoading, error } = useActivities({ fitnessElement: filter || undefined })
  const filterLabel = fitnessFilters.find(([value]) => value === filter)?.[1] ?? '맞춤'

  return (
    <AppLayout active="home">
      <section className="relative min-h-52 overflow-hidden rounded-[2rem] bg-gradient-to-br from-[#e8f7f0] to-[#fff3de] p-6">
        <span className="font-label text-sm font-semibold text-on-surface-variant">아이를 위한 맞춤 활동</span>
        <h1 className="mt-4 font-display text-[28px] leading-tight tracking-[-.09em]">
          오늘은 어떤 놀이를
          <br />
          해볼까요?
        </h1>
        <div
          role="img"
          aria-label="활동 일러스트 영역"
          className="absolute bottom-5 right-6 size-28 rounded-full bg-white/25"
        />
      </section>
      <div className="my-5 flex gap-2 overflow-x-auto pb-1">
        {fitnessFilters.map(([value, label]) => (
          <PillButton key={value || 'all'} active={filter === value} onClick={() => setFilter(value)}>
            {label}
          </PillButton>
        ))}
      </div>
      <SectionTitle
        title={`${filterLabel} 추천`}
        action={<span className="text-xs text-on-surface-variant">{activities.length}개</span>}
      />
      <div className="mt-4 grid gap-3">
        {isLoading && <p className="py-8 text-center text-sm text-on-surface-variant">활동을 불러오고 있어요…</p>}
        {error && (
          <p className="rounded-2xl bg-error-container px-4 py-3 text-sm text-on-error-container">
            활동을 불러오지 못했어요.
          </p>
        )}
        {!isLoading && !error && activities.length === 0 && (
          <p className="py-8 text-center text-sm text-on-surface-variant">추천할 활동이 아직 없어요.</p>
        )}
        {activities.map((activity) => (
          <Card key={activity.id} className="flex items-center gap-3 p-3">
            <div className="grid size-[86px] flex-none place-items-center rounded-2xl bg-gradient-to-br from-[#d8f2e6] to-[#f8dfc8] text-5xl">
              <Icon name={activity.icon} className="text-5xl text-primary" />
            </div>
            <div className="min-w-0 flex-1">
              <span className="font-label text-xs text-on-surface-variant">
                {activity.category} · {activity.description}
              </span>
              <h3 className="mt-1 truncate font-display text-base font-bold tracking-[-.06em]">{activity.title}</h3>
              <p className="mt-2 flex items-center gap-1 text-[11px] text-on-surface-variant">
                <Icon name="sports_score" className="text-sm" />
                공공 추천 콘텐츠
              </p>
            </div>
            {activity.url ? (
              <a
                className="rounded-full p-2 text-primary"
                href={activity.url}
                target="_blank"
                rel="noreferrer"
                aria-label={`${activity.title} 외부 콘텐츠 열기`}
              >
                <Icon name="open_in_new" />
              </a>
            ) : (
              <span className="p-2 text-outline" aria-label="콘텐츠 링크 없음">
                <Icon name="chevron_right" />
              </span>
            )}
          </Card>
        ))}
      </div>
    </AppLayout>
  )
}
