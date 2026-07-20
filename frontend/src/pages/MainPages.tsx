import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AppLayout, Card, GradeBadge, SectionTitle } from '../components/AppLayout'
import { Character } from '../components/Character'
import { Icon } from '../components/Icon'
import { PrimaryButton } from '../components/Button'
import { useChild } from '../hooks/useFitnessData'

export function OnboardingPage() {
  const navigate = useNavigate()
  const [gender, setGender] = useState<'male' | 'female'>('male')
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
            <p className="font-label text-xs font-semibold text-on-surface-variant">처음이시라면</p>
            <h2 className="font-display text-lg font-bold tracking-[-.06em]">아이 프로필을 등록해요</h2>
          </div>
        </div>
        <div className="mb-5 flex gap-2">
          <button className="flex items-center gap-1.5 rounded-full border-2 border-primary bg-primary-container py-1.5 pl-1.5 pr-3 text-sm font-semibold text-primary">
            <span className="grid size-8 place-items-center rounded-full bg-[#ffd7c9] text-primary">
              <span aria-hidden="true" className="size-4 rounded-full bg-white/55" />
            </span>
            망고
          </button>
          <button className="flex items-center gap-1.5 rounded-full border border-outline-variant bg-white py-1.5 pl-1.5 pr-3 text-sm text-on-surface-variant">
            <span className="grid size-8 place-items-center rounded-full bg-[#ffd8dd] text-secondary">
              <span aria-hidden="true" className="size-4 rounded-full bg-white/55" />
            </span>
            하윤
          </button>
          <button className="grid size-11 place-items-center rounded-full border border-dashed border-outline text-outline">
            <Icon name="add" />
          </button>
        </div>
        <form
          onSubmit={(event) => {
            event.preventDefault()
            navigate('/dashboard')
          }}
          className="space-y-4"
        >
          <label className="block">
            <span className="mb-2 block font-label text-xs font-semibold text-on-surface-variant">아이 이름</span>
            <input
              className="h-[52px] w-full rounded-full border border-outline-variant/50 bg-[#fffdf5] px-5 outline-none focus:border-primary focus:ring-4 focus:ring-primary-container/50"
              defaultValue="망고"
            />
          </label>
          <div>
            <span className="mb-2 block font-label text-xs font-semibold text-on-surface-variant">성별</span>
            <div className="flex gap-1 rounded-full bg-surface-container-low p-1">
              <button
                type="button"
                onClick={() => setGender('male')}
                className={`flex h-11 flex-1 items-center justify-center gap-1 rounded-full font-label text-sm ${gender === 'male' ? 'bg-white text-primary shadow-sm' : 'text-on-surface-variant'}`}
              >
                <Icon name="boy" />
                남아
              </button>
              <button
                type="button"
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
              type="month"
              className="h-[52px] w-full rounded-full border border-outline-variant/50 bg-[#fffdf5] px-5 outline-none focus:border-primary"
              defaultValue="2021-09"
            />
          </label>
          <PrimaryButton type="submit" className="mt-2 w-full">
            성장 기록 시작하기
          </PrimaryButton>
        </form>
      </Card>
    </AppLayout>
  )
}

export function HomePage() {
  const navigate = useNavigate()
  return (
    <AppLayout active="home">
      <section className="px-1">
        <h1 className="font-display text-[22px] tracking-[-.07em]">망고님, 오늘도 쑥쑥 자라요!</h1>
        <p className="mt-1 text-sm text-on-surface-variant">아이의 작은 변화도 소중한 성장 기록이에요.</p>
      </section>
      <Card className="mt-5 flex min-h-48 items-center justify-between overflow-hidden bg-gradient-to-br from-white to-[#f5faf7] p-7">
        <div>
          <span className="font-label text-sm text-on-surface-variant">현재 성장 등급</span>
          <h2 className="mt-3 flex items-center gap-2 font-display text-[22px] text-primary">
            <span className="grid size-10 place-items-center rounded-full bg-primary-container">
              <Icon name="seedling" />
            </span>
            새싹 등급
          </h2>
          <p className="mt-3 leading-7 text-on-surface-variant">
            다음 등급인 ‘꽃’까지
            <br />
            <strong className="text-primary">12포인트</strong> 남았어요.
          </p>
        </div>
        <Character />
      </Card>
      <section className="mt-8">
        <SectionTitle
          title="최근 활동 기록"
          action={
            <button className="font-display text-sm font-bold text-primary" onClick={() => navigate('/records')}>
              전체보기
            </button>
          }
        />
        <div className="mt-4 grid grid-cols-2 gap-4">
          <ActivityTile
            icon="directions_run"
            title="셔틀런"
            value="15회 성공"
            tone="coral"
            onClick={() => navigate('/records')}
          />
          <ActivityTile
            icon="arrow_up_double"
            title="제자리멀리뛰기"
            value="110cm"
            tone="mint"
            note="지난번보다 5cm ↑"
            onClick={() => navigate('/records')}
          />
        </div>
      </section>
      <section className="mt-8">
        <h2 className="mb-4 font-display text-[21px] tracking-[-.07em]">오늘의 성장 팁</h2>
        <Card className="border-[#ebe4ce] bg-[#f7f3e7] p-7">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-white px-4 py-2 text-sm text-on-surface-variant">
            <Icon name="lightbulb" />
            놀이 가이드
          </span>
          <h3 className="mt-5 font-display text-xl tracking-[-.07em]">아이와 함께하는 ‘풍선 배구’</h3>
          <p className="mt-3 leading-8 text-on-surface-variant">
            실내에서 안전하게 민첩성과 협응력을 길러주세요. 풍선이 땅에 닿지 않게 주고받으며 자연스럽게 움직임을
            유도합니다.
          </p>
          <PrimaryButton className="mt-1" onClick={() => navigate('/activities')}>
            자세히 알아보기
          </PrimaryButton>
          <div className="mt-6 grid h-28 place-items-center rounded-3xl bg-gradient-to-br from-[#dcefdc] to-[#f5dfc7]">
            <span aria-hidden="true" className="size-16 rounded-[38%] bg-white/25" />
          </div>
        </Card>
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
        className="fixed bottom-24 right-[max(24px,calc(50%_-_220px))] z-20 grid size-14 place-items-center rounded-full bg-primary text-white shadow-lg"
        onClick={() => navigate('/diagnosis/input')}
      >
        <Icon name="add_task" />
      </button>
    </AppLayout>
  )
}

function ActivityTile({
  icon,
  title,
  value,
  tone,
  note,
  onClick,
}: {
  icon: string
  title: string
  value: string
  tone: 'mint' | 'coral'
  note?: string
  onClick: () => void
}) {
  return (
    <button
      className="min-h-48 rounded-3xl border border-outline-variant/40 bg-white p-5 text-left shadow-soft"
      onClick={onClick}
    >
      <span
        className={`mb-5 grid size-12 place-items-center rounded-full ${tone === 'mint' ? 'bg-[#e1f7ef] text-primary' : 'bg-[#ffe1df] text-secondary'}`}
      >
        <Icon name={icon} />
      </span>
      <h3 className="font-display text-base font-medium tracking-[-.06em]">{title}</h3>
      <p className="mt-2 text-sm">{value}</p>
      {note ? (
        <span className="mt-4 block text-sm leading-6 text-primary">↗ {note}</span>
      ) : (
        <span className="mt-4 block h-1 rounded-full bg-surface-container-high">
          <span className="block h-full w-3/4 rounded-full bg-secondary" />
        </span>
      )}
    </button>
  )
}

export function DashboardPage() {
  const navigate = useNavigate()
  const { data: child } = useChild()
  return (
    <AppLayout active="home">
      <section className="pt-2 text-center">
        <div className="mx-auto w-fit">
          <Character large />
        </div>
        <div className="-mt-1">
          <GradeBadge />
          <h1 className="mt-2 font-display text-[28px] font-bold tracking-[-.09em]">
            {child?.name ?? '망고'}의 성장 일기
          </h1>
          <p className="mt-2 text-base text-on-surface-variant">건강하게 쑥쑥 자라나고 있어요!</p>
        </div>
      </section>
      <Card className="mt-9 border-l-4 border-l-primary p-7">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="font-display text-2xl font-bold tracking-[-.08em]">최근 진단 기록</h2>
            <p className="mt-2 text-[17px] text-on-surface-variant">2023년 10월 24일 측정</p>
          </div>
          <Icon name="analytics" className="text-primary" />
        </div>
        <div className="mt-5 flex flex-wrap gap-2">
          <span className="inline-flex items-center gap-1 rounded-full bg-primary-container px-4 py-2 text-sm text-primary">
            <Icon name="flashlight" className="text-base" />
            순발력 왕
          </span>
          <span className="inline-flex items-center gap-1 rounded-full bg-primary-container px-4 py-2 text-sm text-primary">
            <Icon name="run" className="text-base" />
            유연성 최고
          </span>
          <span className="inline-flex items-center gap-1 rounded-full bg-[#ffd9d5] px-4 py-2 text-sm text-secondary">
            <Icon name="fitness_center" className="text-base" />
            근력 부족
          </span>
        </div>
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
  const bars = [
    ['송파구', 82],
    ['강남구', 71],
    ['서초구', 64],
    ['마포구', 53],
    ['용산구', 45],
  ] as const
  return (
    <AppLayout active="centers">
      <PageHeading
        eyebrow="우리 동네 데이터"
        title="서울시 참여율 랭킹"
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
            송파구 상위 1위
          </span>
          <h2 className="mt-3 font-display text-xl font-bold leading-tight text-primary">
            우리 동네는
            <br />
            <strong>참여가 활발해요!</strong>
          </h2>
          <p className="mt-2 text-xs leading-5 text-primary">
            전국 평균보다 18% 높은
            <br />
            측정 참여율을 보이고 있어요.
          </p>
        </div>
      </Card>
      <Card className="mt-5 p-5">
        <SectionTitle
          title="지역별 참여율"
          action={
            <button className="rounded-full bg-surface-container-low px-3 py-2 text-xs text-on-surface-variant">
              서울시 <Icon name="expand_more" className="text-base" />
            </button>
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
        <div className="relative mt-4 h-56 overflow-hidden rounded-2xl bg-gradient-to-br from-[#dff4e8] to-[#fff3e2]">
          <div className="absolute left-0 top-0 h-24 w-32 rounded-[14px_38px_18px_25px] bg-[#c8ebdc] p-8 text-xs">
            강북구
          </div>
          <div className="absolute left-24 top-6 h-24 w-24 rotate-6 bg-[#e9f5df] p-8 text-xs">종로구</div>
          <div className="absolute right-2 top-2 h-20 w-24 rounded-[40px_14px_28px_16px] bg-[#ffddca] p-7 text-xs">
            중구
          </div>
          <div className="absolute bottom-[-10px] left-12 h-24 w-32 rounded-[42px_15px_10px_40px] bg-[#9bd9bb] p-8 text-xs">
            강남구
          </div>
          <div className="absolute bottom-5 right-[-10px] h-20 w-28 rounded-[18px_55px_20px_12px] bg-[#f2c8bc] p-8 text-xs">
            송파구
          </div>
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
