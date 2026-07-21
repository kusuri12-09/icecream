import { useState, type FormEvent } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { ApiError } from '../api/client'
import { AppLayout, Card, GradeBadge, SectionTitle } from '../components/AppLayout'
import { Icon } from '../components/Icon'
import { PrimaryButton, PillButton } from '../components/Button'
import { useChild, useCreateMeasurement } from '../hooks/useFitnessData'
import type { MeasurementResult } from '../types/models'

export function DiagnosisPage() {
  const navigate = useNavigate()
  const [selected, setSelected] = useState('flexibility')
  return (
    <AppLayout active="diagnosis">
      <section className="px-2 pb-7">
        <h1 className="font-display text-[28px] leading-tight tracking-[-.09em]">
          우리 아이의
          <br />
          성장을 진단해요
        </h1>
        <p className="mt-4 text-base leading-7 text-on-surface-variant">
          국가 표준 체력 측정 기준에 따라
          <br />
          부드럽게, 그리고 꼼꼼하게 체크합니다.
        </p>
      </section>
      <div className="grid grid-cols-2 gap-4">
        <DiagnosisCategory
          wide={true}
          tone="mint"
          active={selected === 'strength'}
          onClick={() => setSelected('strength')}
          icon="fitness_center"
          title="근력 및 근지구력"
          description="윗몸 말아 올리기 외 2건"
        />
        <DiagnosisCategory
          tone="coral"
          active={selected === 'power'}
          onClick={() => setSelected('power')}
          icon="directions_run"
          title="순발력"
          description="제자리 멀리뛰기"
        />
        <DiagnosisCategory
          tone="cream"
          active={selected === 'flexibility'}
          onClick={() => setSelected('flexibility')}
          icon="accessibility_new"
          title="유연성"
          description="앉아 윗몸 굽히기"
        />
      </div>
      <Card className="mt-7 p-7">
        <SectionTitle
          title="앉아 윗몸 굽히기"
          action={
            <span className="grid size-9 place-items-center rounded-xl bg-primary-container text-primary">
              <Icon name="straighten" />
            </span>
          }
        />
        <div className="relative mt-5 grid h-48 place-items-center overflow-hidden rounded-[2rem] bg-gradient-to-br from-[#bde8df] to-[#f1eee1]">
          <div
            role="img"
            aria-label="측정 안내 이미지 영역"
            className="size-28 rounded-full border-4 border-white/55 bg-white/20"
          />
          <span className="absolute bottom-3 left-3 right-3 flex items-center justify-center gap-1 rounded-full bg-white/80 px-2 py-2 text-xs text-primary">
            <Icon name="info" className="text-base" />
            무릎을 펴고 천천히 밀어주세요
          </span>
        </div>
        <label className="mt-6 block">
          <span className="mb-3 block text-lg">측정값 (cm)</span>
          <div className="flex h-24 items-center justify-center gap-20 rounded-full bg-surface-container-low text-xl text-outline-variant">
            <span>00.0</span>
            <b className="text-sm font-normal text-on-surface">cm</b>
          </div>
        </label>
        <p className="mt-5 text-center text-lg leading-7">
          아이의 유연성은 성장의 중요한 지표예요!
          <br />
          <Icon name="sparkling" className="text-primary" />
        </p>
      </Card>
      <PrimaryButton className="mt-8 w-full" onClick={() => navigate('/diagnosis/result')}>
        진단 결과 저장하기
      </PrimaryButton>
    </AppLayout>
  )
}

function DiagnosisCategory({
  wide = false,
  tone,
  active,
  onClick,
  icon,
  title,
  description,
}: {
  wide?: boolean
  tone: 'mint' | 'coral' | 'cream'
  active: boolean
  onClick: () => void
  icon: string
  title: string
  description: string
}) {
  const styles = {
    mint: 'bg-primary-container text-primary',
    coral: 'bg-secondary-container text-secondary',
    cream: 'bg-tertiary-container text-[#625f4e]',
  }
  return (
    <button
      onClick={onClick}
      className={`${wide ? 'col-span-2 min-h-44' : 'min-h-36'} rounded-[2.5rem] p-6 text-left transition hover:-translate-y-0.5 ${styles[tone]} ${active ? 'ring-4 ring-primary/20' : ''}`}
    >
      <Icon name={icon} />
      <b className="mt-5 block text-lg font-normal tracking-[-.06em]">{title}</b>
      <span className="mt-1 block leading-6">{description}</span>
    </button>
  )
}

export function DiagnosisResultPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { data: child } = useChild()
  const routeState = location.state as { measurement?: MeasurementResult } | null
  const result = routeState?.measurement
  const strengths = result?.profile.strengths.length ? result.profile.strengths : ['유연성']
  const weaknesses = result?.profile.weaknesses.length ? result.profile.weaknesses : ['근력']

  return (
    <AppLayout active="diagnosis" back>
      <section className="px-2 pb-9 text-center">
        <div
          role="img"
          aria-label="진단 결과 일러스트 영역"
          className="mx-auto mb-4 size-40 rounded-full border-[5px] border-primary-container bg-white shadow-[0_0_42px_rgba(181,234,215,.35)]"
        />
        <GradeBadge dark grade={result?.grade ?? '새싹'} />
        <h1 className="mt-4 font-display text-[27px] font-bold tracking-[-.1em]">
          {child?.name ?? '아이'}님, 무럭무럭 자라고 있어요!
        </h1>
        <p className="mt-3 text-base leading-7 text-on-surface-variant">
          {result ? `${result.items.length}개 측정 항목을 바탕으로 등급을 판정했어요.` : '기초 체력이 눈에 띄게 좋아졌네요.'}
          <br />
          작은 습관들이 열매를 맺기 시작했어요.
        </p>
      </section>
      <Card className="p-7">
        <SectionTitle
          title="성장 프로필"
          action={
            <span className="grid size-9 place-items-center rounded-xl bg-primary-container text-primary">
              <Icon name="analytics" />
            </span>
          }
        />
        <RadarFigure />
        <div className="mt-4 grid grid-cols-2 gap-4">
          <div className="rounded-lg bg-[#effaf6] p-4 text-center">
            <span className="block text-sm text-primary">장점</span>
            <b className="mt-1 block font-normal">{strengths[0]}</b>
          </div>
          <div className="rounded-lg bg-[#fff0ef] p-4 text-center text-secondary">
            <span className="block text-sm">개선 필요</span>
            <b className="mt-1 block font-normal">{weaknesses[0]}</b>
          </div>
        </div>
      </Card>
      <Card className="mt-4 p-6">
        <span className="inline-flex items-center gap-1.5 rounded-full bg-primary-container px-4 py-2 text-sm text-primary">
          <Icon name="directions_run" />
          맞춤 활동
        </span>
        <h2 className="mt-4 font-display text-xl tracking-[-.07em]">근력을 재미있게 키워볼까요?</h2>
        <p className="mt-2 text-sm text-on-surface-variant">아이의 현재 결과에 맞춘 놀이를 추천해드려요.</p>
        <button
          className="mt-4 inline-flex items-center gap-1 font-semibold text-primary"
          onClick={() => navigate('/activities')}
        >
          활동 추천 보기 <Icon name="arrow_forward" />
        </button>
      </Card>
    </AppLayout>
  )
}
function RadarFigure() {
  return (
    <div className="relative mx-auto my-4 h-80 max-w-[310px] rounded-full bg-[repeating-radial-gradient(circle_at_center,transparent_0_41px,rgba(108,128,118,.16)_42px_44px),linear-gradient(rgba(108,128,118,.14),rgba(108,128,118,.14))_center/1px_100%_no-repeat,linear-gradient(90deg,rgba(108,128,118,.14),rgba(108,128,118,.14))_center/100%_1px_no-repeat]">
      <span className="absolute left-1/2 top-0 -translate-x-1/2 text-sm text-on-surface-variant">유연성</span>
      <span className="absolute right-[-4px] top-1/2 -translate-y-1/2 text-sm text-on-surface-variant">근력</span>
      <span className="absolute bottom-0 left-1/2 -translate-x-1/2 text-sm text-on-surface-variant">지구력</span>
      <span className="absolute left-[-10px] top-1/2 -translate-y-1/2 text-sm text-on-surface-variant">균형감</span>
      <div className="absolute inset-[65px_38px] [clip-path:polygon(50%_0,100%_50%,50%_100%,0_50%)] border-[6px] border-primary bg-primary-container/50" />
    </div>
  )
}

const measurementFields = [
  { itemKey: 'CARDIO', group: '심폐지구력', label: '10m 왕복 오래달리기', unit: '회', icon: 'directions_run' },
  { itemKey: 'GRIP', group: '근력', label: '상대악력', unit: '%', icon: 'fitness_center' },
  { itemKey: 'MUSCULAR_END', group: '근지구력', label: '윗몸 말아올리기', unit: '회', icon: 'self_improvement' },
  { itemKey: 'FLEXIBILITY', group: '유연성', label: '앉아 윗몸 앞으로 굽히기', unit: 'cm', icon: 'straighten' },
  { itemKey: 'AGILITY', group: '민첩성', label: '5m × 4 왕복달리기', unit: '초', icon: 'directions_run' },
  { itemKey: 'POWER', group: '순발력', label: '제자리 멀리뛰기', unit: 'cm', icon: 'bolt' },
  { itemKey: 'COORDINATION', group: '협응력', label: '3×3 버튼 누르기', unit: '초', icon: 'touch_app' },
  { itemKey: 'BMI', group: '신체조성', label: 'BMI', unit: '', icon: 'monitor_weight' },
] as const

export function MeasurementInputPage() {
  const navigate = useNavigate()
  const { data: child } = useChild()
  const createMeasurement = useCreateMeasurement()
  const [type, setType] = useState<'official' | 'self'>('official')
  const [values, setValues] = useState<Record<string, string>>({})
  const [measuredAt, setMeasuredAt] = useState(() => new Date().toISOString().slice(0, 10))
  const [centerId, setCenterId] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    if (!child?.id) {
      setError('먼저 아이 프로필을 등록해주세요.')
      return
    }
    if (!measuredAt) {
      setError('측정일을 선택해주세요.')
      return
    }

    const items: Array<{ itemKey: string; value: number }> = []
    for (const field of measurementFields) {
      const rawValue = values[field.itemKey]?.trim()
      if (!rawValue) continue
      const value = Number(rawValue)
      if (!Number.isFinite(value) || value < 0) {
        setError(`${field.group} 측정값을 0 이상의 숫자로 입력해주세요.`)
        return
      }
      items.push({ itemKey: field.itemKey, value })
    }
    if (items.length === 0) {
      setError('측정값을 하나 이상 입력해주세요.')
      return
    }

    try {
      const result = await createMeasurement.mutateAsync({
        childId: child.id,
        request: {
          type: type === 'official' ? 'OFFICIAL' : 'SELF',
          measuredAt,
          centerId: type === 'official' ? centerId.trim() || null : null,
          items,
        },
      })
      navigate('/diagnosis/result', { replace: true, state: { measurement: result } })
    } catch (cause) {
      if (cause instanceof ApiError && cause.status === 401) {
        navigate('/login', { replace: true })
        return
      }
      setError(cause instanceof ApiError ? cause.message : '측정 결과를 저장하지 못했습니다. 잠시 후 다시 시도해주세요.')
    }
  }

  function updateValue(itemKey: string, value: string) {
    setValues((current) => ({ ...current, [itemKey]: value }))
  }

  return (
    <AppLayout active="diagnosis">
      <section className="px-2 pb-5">
        <span className="font-label text-sm font-semibold text-on-surface-variant">{child?.name ?? '아이'}의 오늘</span>
        <h1 className="mt-2 font-display text-[28px] tracking-[-.09em]">체력 측정 입력</h1>
        <p className="mt-3 text-base leading-7 text-on-surface-variant">
          측정 결과를 입력하면 성장 등급과
          <br />
          항목별 강점을 확인할 수 있어요.
        </p>
      </section>
      <form className="grid gap-4" onSubmit={handleSubmit}>
        <div className="flex gap-1 rounded-full bg-surface-container-low p-1">
          <PillButton className="flex-1 border-0" active={type === 'official'} onClick={() => setType('official')}>
            정식 측정
          </PillButton>
          <PillButton className="flex-1 border-0" active={type === 'self'} onClick={() => setType('self')}>
            자가측정
          </PillButton>
        </div>
        {type === 'self' && (
          <div className="flex items-center gap-2 rounded-2xl bg-[#e9f7f1] p-4 text-sm text-primary">
            <Icon name="info" />
            <span>자가측정 결과는 참고용으로만 활용돼요.</span>
          </div>
        )}
        <label className="grid gap-2 text-sm font-semibold">
          측정일
          <input
            type="date"
            value={measuredAt}
            onChange={(event) => setMeasuredAt(event.target.value)}
            className="h-[52px] rounded-full border border-outline-variant/50 bg-white px-5 font-normal outline-none focus:border-primary"
          />
        </label>
        {type === 'official' && (
          <label className="grid gap-2 text-sm font-semibold">
            센터 ID <span className="font-normal text-on-surface-variant">(선택)</span>
            <input
              value={centerId}
              onChange={(event) => setCenterId(event.target.value)}
              className="h-[52px] rounded-full border border-outline-variant/50 bg-white px-5 font-normal outline-none focus:border-primary"
              placeholder="center_45"
            />
          </label>
        )}
        <div className="grid gap-2.5">
          {measurementFields.map((field, index) => (
            <label
              key={field.itemKey}
              className="flex min-h-[82px] items-center gap-3 rounded-[22px] border border-outline-variant/40 bg-white p-3 shadow-soft"
            >
              <span
                className={`grid size-11 flex-none place-items-center rounded-xl ${index % 3 === 1 ? 'bg-[#ffe2df] text-secondary' : index % 3 === 2 ? 'bg-tertiary-container text-[#625f4e]' : 'bg-primary-container text-primary'}`}
              >
                <Icon name={field.icon} />
              </span>
              <span className="min-w-0 flex-1">
                <b className="block text-base">{field.group}</b>
                <small className="mt-1 block truncate text-[11px] text-on-surface-variant">{field.label}</small>
              </span>
              <span className="flex h-11 items-center rounded-full bg-surface-container-low pl-3 pr-2">
                <input
                  value={values[field.itemKey] ?? ''}
                  onChange={(event) => updateValue(field.itemKey, event.target.value)}
                  className="w-14 bg-transparent text-right outline-none"
                  placeholder="00.0"
                  inputMode="decimal"
                  aria-label={`${field.group} 측정값`}
                />
                <em className="text-[11px] not-italic text-on-surface-variant">{field.unit}</em>
              </span>
            </label>
          ))}
        </div>
        {error && (
          <p role="alert" className="rounded-2xl bg-error-container px-4 py-3 text-sm text-on-error-container">
            {error}
          </p>
        )}
        <PrimaryButton type="submit" className="w-full" disabled={createMeasurement.isPending}>
          {createMeasurement.isPending ? '결과를 저장하고 있어요…' : '진단 결과 확인하기'}
        </PrimaryButton>
      </form>
    </AppLayout>
  )
}
