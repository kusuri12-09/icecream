import { useMemo } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { AppLayout, Card, GradeBadge, SectionTitle } from '../components/AppLayout'
import { Icon } from '../components/Icon'
import { useChild, useDeleteMeasurement, useGrowth, useMeasurement, useRecords } from '../hooks/useFitnessData'

export function RecordsPage() {
  const navigate = useNavigate()
  const { data: child } = useChild()
  const { data: records = [], isLoading, error } = useRecords()
  const { data: growth } = useGrowth(child?.id)
  const chartData = useMemo(() => {
    const points = new Map<string, { official: number[]; self: number[] }>()
    for (const series of growth?.series ?? []) {
      for (const point of series.points) {
        const current = points.get(point.measuredAt) ?? { official: [], self: [] }
        current[point.type === 'OFFICIAL' ? 'official' : 'self'].push(point.value)
        points.set(point.measuredAt, current)
      }
    }
    return [...points.entries()]
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([measuredAt, values]) => ({
        month: measuredAt.slice(0, 7).replace('-', '.'),
        official: average(values.official),
        self: average(values.self),
      }))
  }, [growth])

  return (
    <AppLayout active="records">
      <PageIntro
        eyebrow={`${child?.name ?? '아이'}의 성장 기록`}
        title="쑥쑥 자라고 있어요!"
        description={
          <>
            꾸준히 기록할수록 우리 아이의
            <br />
            성장 흐름이 더 선명해져요.
          </>
        }
      />
      <Card className="p-5">
        <SectionTitle title="종합 체력 성장 그래프" />
        <div className="mt-5 h-52">
          {chartData.length ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 12, right: 6, left: -28, bottom: 0 }}>
                <XAxis dataKey="month" tick={{ fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis domain={[0, 'auto']} tick={{ fontSize: 10 }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ borderRadius: 16, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,.08)' }} />
                <Line type="monotone" dataKey="official" name="정식 측정" stroke="#366758" strokeWidth={4} dot={{ r: 4, fill: '#366758' }} connectNulls />
                <Line type="monotone" dataKey="self" name="자가측정 참고" stroke="#f4aaa7" strokeWidth={3} strokeDasharray="5 8" dot={false} connectNulls />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="grid h-full place-items-center text-sm text-on-surface-variant">성장 그래프를 표시할 측정 기록이 없어요.</div>
          )}
        </div>
        <div className="mt-2 flex justify-center gap-4 text-[11px] text-on-surface-variant">
          <span className="flex items-center gap-1"><i className="w-5 border-t-[3px] border-primary" />정식 측정</span>
          <span className="flex items-center gap-1"><i className="w-5 border-t-[3px] border-dashed border-[#f4aaa7]" />자가측정 참고</span>
        </div>
      </Card>
      <section className="mt-8">
        <SectionTitle title="과거 진단 기록" />
        <div className="mt-3 grid gap-2">
          {isLoading && <p className="py-6 text-center text-sm text-on-surface-variant">기록을 불러오고 있어요…</p>}
          {error && <p className="rounded-2xl bg-error-container px-4 py-3 text-sm text-on-error-container">기록을 불러오지 못했어요.</p>}
          {!isLoading && !error && records.length === 0 && <p className="py-6 text-center text-sm text-on-surface-variant">아직 진단 기록이 없어요.</p>}
          {records.map((record) => (
            <button
              className="flex items-center gap-3 rounded-[20px] border border-outline-variant/40 bg-white p-3.5 text-left shadow-soft"
              key={record.id}
              onClick={() => navigate(`/records/${record.id}`)}
            >
              <span className="flex-1 text-sm">
                {record.date}
                <small className="mt-1 block text-[10px] text-on-surface-variant">{record.type === 'official' ? '정식 측정' : '자가측정 참고'}</small>
              </span>
              <span className="text-xs text-primary"><Icon name="seedling" /> {record.grade} 등급</span>
              <b>{record.score == null ? '상세' : `${Math.round(record.score)}점`}</b>
              <Icon name="chevron_right" className="text-lg text-outline" />
            </button>
          ))}
        </div>
      </section>
    </AppLayout>
  )
}

function average(values: number[]) {
  return values.length ? Math.round((values.reduce((sum, value) => sum + value, 0) / values.length) * 10) / 10 : undefined
}

export function MeasurementDetailPage() {
  const navigate = useNavigate()
  const { measurementId } = useParams()
  const { data: measurement, isLoading, error } = useMeasurement(measurementId)
  const deleteMutation = useDeleteMeasurement()

  async function handleDelete() {
    if (!measurement || !window.confirm('이 측정 기록을 삭제할까요?')) return
    await deleteMutation.mutateAsync({ measurementId: measurement.id, childId: measurement.childId })
    navigate('/records', { replace: true })
  }

  if (isLoading) {
    return <AppLayout active="records" back><div className="grid min-h-[50vh] place-items-center text-sm text-on-surface-variant">상세 기록을 불러오고 있어요…</div></AppLayout>
  }
  if (error || !measurement) {
    return <AppLayout active="records" back><p className="rounded-2xl bg-error-container p-4 text-sm text-on-error-container">측정 기록을 불러오지 못했어요.</p></AppLayout>
  }

  return (
    <AppLayout active="records" back>
      <PageIntro eyebrow="측정 상세" title={`${measurement.measuredAt} 기록`} description="측정 항목별 결과와 성장 프로필을 확인해보세요." />
      <Card className="p-6">
        <div className="flex items-center justify-between"><GradeBadge grade={measurement.grade} /><span className="text-sm text-on-surface-variant">{measurement.type === 'official' ? '정식 측정' : '자가측정'}</span></div>
        <div className="mt-6 grid gap-2">
          {measurement.items.map((item) => (
            <div key={item.itemKey} className="flex items-center gap-3 rounded-2xl bg-surface-container-low p-3">
              <span className="flex-1 text-sm">{item.label || item.itemKey}</span>
              <b>{item.value}</b>
              {item.isWeak && <span className="text-xs text-secondary">개선 필요</span>}
            </div>
          ))}
        </div>
      </Card>
      <button type="button" onClick={handleDelete} disabled={deleteMutation.isPending} className="mt-4 w-full rounded-full border border-error/40 px-5 py-3 text-sm text-error disabled:opacity-50">
        {deleteMutation.isPending ? '삭제하고 있어요…' : '측정 기록 삭제'}
      </button>
    </AppLayout>
  )
}
export function GrowthPage() {
  const { data: child } = useChild()
  const { data: growth } = useGrowth(child?.id)
  const metricColors = ['bg-primary', 'bg-secondary', 'bg-[#b4ad8d]', 'bg-primary'] as const
  const metrics = (growth?.series ?? []).slice(0, 4).map((series, index) => {
    const latest = series.points.at(-1)
    const previous = series.points.at(-2)
    const score = latest ? `${Math.min(100, Math.round(latest.value))}%` : '-'
    const change = latest && previous ? `${latest.value - previous.value >= 0 ? '+' : ''}${Math.round(latest.value - previous.value)}%` : ''
    return [series.label, score, change, metricColors[index % metricColors.length]] as const
  })
  const overallScore = metrics[0]?.[1] ?? '-'

  return (
    <AppLayout active="records">
      <PageIntro
        eyebrow="성장 리포트"
        title={`${child?.name ?? '아이'}의 변화가 보여요`}
        description={
          <>
            지난 측정과 비교해 좋아진 점을
            <br />
            한눈에 확인해보세요.
          </>
        }
      />
      <Card className="flex items-center gap-5 bg-gradient-to-br from-white to-[#f0fbf6] p-6">
        <div className="grid size-28 flex-none place-items-center rounded-full border-[10px] border-primary-container border-r-primary">
          <b className="font-display text-3xl text-primary">{overallScore}</b>
          <small className="-mt-1 text-[10px] text-on-surface-variant">종합 점수</small>
        </div>
        <div>
          <span className="rounded-full bg-primary-container px-3 py-2 text-xs text-primary">
            {growth?.gradeHistory.at(-1)?.grade ?? '측정 기록을 불러오는 중이에요'}
          </span>
          <h2 className="mt-4 font-display text-xl">성장 추이</h2>
          <p className="mt-1 text-xs leading-5 text-on-surface-variant">
            측정 기록을 바탕으로
            <br />
            성장 흐름을 확인해보세요.
          </p>
        </div>
      </Card>
      <section className="mt-7">
        <SectionTitle title="항목별 변화" />
        <div className="mt-3 grid gap-2">
          {metrics.map(([name, score, change, color]) => (
            <div
              key={name}
              className="grid min-h-[70px] grid-cols-[95px_1fr_38px_40px] items-center gap-2 rounded-[20px] border border-outline-variant/40 bg-white p-3.5 shadow-soft"
            >
              <span className="flex items-center gap-2 text-xs">
                <i className="grid size-8 place-items-center rounded-xl bg-primary-container text-primary">
                  <Icon name="trending_up" className="text-base" />
                </i>
                {name}
              </span>
              <span className="h-2 overflow-hidden rounded-full bg-surface-container">
                <i className={`block h-full rounded-full ${color}`} style={{ width: score === '-' ? '0%' : score }} />
              </span>
              <strong className="text-right text-xs">{score}</strong>
              <em className="text-right text-[11px] not-italic text-primary">{change}</em>
            </div>
          ))}
        </div>
      </section>
      <Card className="mt-5 p-5">
        <span className="inline-flex items-center gap-1 rounded-full bg-surface-container-low px-3 py-2 text-xs text-on-surface-variant">
          <Icon name="flag" className="text-base" />
          다음 목표
        </span>
        <h2 className="mt-4 font-display text-lg">다음 성장 단계를 향해 가고 있어요</h2>
        <div className="mt-4 h-2.5 rounded-full bg-surface-container">
          <span className="block h-full w-3/4 rounded-full bg-gradient-to-r from-primary-container to-primary" />
        </div>
        <p className="mt-3 text-xs text-on-surface-variant">측정 기록이 쌓일수록 변화가 더 선명해져요.</p>
      </Card>
    </AppLayout>
  )
}
function PageIntro({ eyebrow, title, description }: { eyebrow: string; title: string; description: React.ReactNode }) {
  return (
    <section className="px-2 pb-6">
      <span className="font-label text-sm font-semibold text-on-surface-variant">{eyebrow}</span>
      <h1 className="mt-2 font-display text-[28px] leading-tight tracking-[-.09em]">{title}</h1>
      <p className="mt-3 text-base leading-7 text-on-surface-variant">{description}</p>
    </section>
  )
}
