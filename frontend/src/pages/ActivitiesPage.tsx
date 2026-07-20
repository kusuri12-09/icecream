import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AppLayout, Card, SectionTitle } from '../components/AppLayout'
import { Icon } from '../components/Icon'
import { PillButton } from '../components/Button'
import { useActivities } from '../hooks/useFitnessData'

export function ActivitiesPage() {
  const { data: activities = [] } = useActivities()
  const [filter, setFilter] = useState('전체')
  const navigate = useNavigate()
  const filtered = useMemo(
    () =>
      filter === '전체'
        ? activities
        : filter === '기구 필요'
          ? activities.filter((item) => item.equipment)
          : activities.filter((item) => item.place === filter),
    [activities, filter],
  )
  return (
    <AppLayout active="home">
      <section className="relative min-h-52 overflow-hidden rounded-[2rem] bg-gradient-to-br from-[#e8f7f0] to-[#fff3de] p-6">
        <span className="font-label text-sm font-semibold text-on-surface-variant">지우를 위한 맞춤 활동</span>
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
        {['전체', '실내', '야외', '기구 필요'].map((item) => (
          <PillButton key={item} active={filter === item} onClick={() => setFilter(item)}>
            {item}
          </PillButton>
        ))}
      </div>
      <SectionTitle
        title="근력 부족을 위한 추천"
        action={<span className="text-xs text-on-surface-variant">{filtered.length}개</span>}
      />
      <div className="mt-4 grid gap-3">
        {filtered.map((activity) => (
          <Card key={activity.id} className="flex items-center gap-3 p-3">
            <div className="grid size-[86px] flex-none place-items-center rounded-2xl bg-gradient-to-br from-[#d8f2e6] to-[#f8dfc8] text-5xl">
              <Icon name={activity.icon} className="text-5xl text-primary" />
            </div>
            <div className="min-w-0 flex-1">
              <span className="font-label text-xs text-on-surface-variant">
                {activity.category} · {activity.place}
              </span>
              <h3 className="mt-1 truncate font-display text-base font-bold tracking-[-.06em]">{activity.title}</h3>
              <p className="mt-2 flex items-center gap-1 text-[11px] text-on-surface-variant">
                <Icon name="schedule" className="text-sm" />
                {activity.duration} · 쉬운 난이도
              </p>
            </div>
            <button
              className="text-outline"
              onClick={() => navigate('/diagnosis/result')}
              aria-label={`${activity.title} 상세`}
            >
              <Icon name="chevron_right" />
            </button>
          </Card>
        ))}
      </div>
    </AppLayout>
  )
}
