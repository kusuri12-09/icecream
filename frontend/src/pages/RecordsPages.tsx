import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { AppLayout, Card, SectionTitle } from '../components/AppLayout'
import { Icon } from '../components/Icon'
import { useRecords } from '../hooks/useFitnessData'

const chartData = [
  { month: '2023.01', official: 42, self: 36 },
  { month: '2023.04', official: 49, self: 40 },
  { month: '2023.07', official: 58, self: 47 },
  { month: '2023.10', official: 72, self: 61 },
]

export function RecordsPage() {
  const { data: records = [] } = useRecords()
  return (
    <AppLayout active="records">
      <PageIntro
        eyebrow="망고의 성장 기록"
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
        <SectionTitle
          title="종합 체력 성장 그래프"
          action={
            <button className="rounded-full bg-surface-container-low px-3 py-2 text-xs text-on-surface-variant">
              최근 1년 <Icon name="expand_more" className="text-base" />
            </button>
          }
        />
        <div className="mt-5 h-52">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 12, right: 6, left: -28, bottom: 0 }}>
              <XAxis dataKey="month" tick={{ fontSize: 10 }} axisLine={false} tickLine={false} />
              <YAxis domain={[0, 80]} tick={{ fontSize: 10 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ borderRadius: 16, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,.08)' }} />
              <Line
                type="monotone"
                dataKey="official"
                name="정식 측정"
                stroke="#366758"
                strokeWidth={4}
                dot={{ r: 4, fill: '#366758' }}
              />
              <Line
                type="monotone"
                dataKey="self"
                name="자가측정 참고"
                stroke="#f4aaa7"
                strokeWidth={3}
                strokeDasharray="5 8"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-2 flex justify-center gap-4 text-[11px] text-on-surface-variant">
          <span className="flex items-center gap-1">
            <i className="w-5 border-t-[3px] border-primary" />
            정식 측정
          </span>
          <span className="flex items-center gap-1">
            <i className="w-5 border-t-[3px] border-dashed border-[#f4aaa7]" />
            자가측정 참고
          </span>
        </div>
      </Card>
      <section className="mt-8">
        <SectionTitle
          title="과거 진단 기록"
          action={
            <button className="flex items-center gap-1 text-sm font-bold text-primary">
              전체보기 <Icon name="arrow_forward" className="text-base" />
            </button>
          }
        />
        <div className="mt-3 grid gap-2">
          {records.map((record) => (
            <button
              className="flex items-center gap-3 rounded-[20px] border border-outline-variant/40 bg-white p-3.5 text-left shadow-soft"
              key={record.id}
            >
              <span className="flex-1 text-sm">
                {record.date}
                <small className="mt-1 block text-[10px] text-on-surface-variant">
                  {record.type === 'official' ? '정식 측정' : '자가측정 참고'}
                </small>
              </span>
              <span className="text-xs text-primary">
                <Icon name={record.grade === '새싹' ? 'seedling' : 'seedling'} /> {record.grade} 등급
              </span>
              <b>{record.score}점</b>
              <Icon name="chevron_right" className="text-lg text-outline" />
            </button>
          ))}
        </div>
      </section>
    </AppLayout>
  )
}

export function GrowthPage() {
  const metrics = [
    ['유연성', '94%', '+18%', 'bg-primary'],
    ['순발력', '82%', '+12%', 'bg-secondary'],
    ['근력', '55%', '+8%', 'bg-[#b4ad8d]'],
    ['지구력', '68%', '+15%', 'bg-primary'],
  ] as const
  return (
    <AppLayout active="records">
      <PageIntro
        eyebrow="성장 리포트"
        title="망고의 변화가 보여요"
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
          <b className="font-display text-3xl text-primary">72</b>
          <small className="-mt-1 text-[10px] text-on-surface-variant">종합 점수</small>
        </div>
        <div>
          <span className="rounded-full bg-primary-container px-3 py-2 text-xs text-primary">지난 측정보다 +14점</span>
          <h2 className="mt-4 font-display text-xl">새싹 등급</h2>
          <p className="mt-1 text-xs leading-5 text-on-surface-variant">
            꾸준한 활동으로
            <br />
            기초 체력이 좋아졌어요.
          </p>
        </div>
      </Card>
      <section className="mt-7">
        <SectionTitle
          title="항목별 변화"
          action={
            <button className="rounded-full bg-surface-container-low px-3 py-2 text-xs text-on-surface-variant">
              최근 1년 <Icon name="expand_more" className="text-base" />
            </button>
          }
        />
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
                <i className={`block h-full rounded-full ${color}`} style={{ width: score }} />
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
        <h2 className="mt-4 font-display text-lg">꽃 등급까지 12포인트</h2>
        <div className="mt-4 h-2.5 rounded-full bg-surface-container">
          <span className="block h-full w-3/4 rounded-full bg-gradient-to-r from-primary-container to-primary" />
        </div>
        <p className="mt-3 text-xs text-on-surface-variant">조금만 더 힘내면 다음 성장 단계에 도달해요!</p>
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
