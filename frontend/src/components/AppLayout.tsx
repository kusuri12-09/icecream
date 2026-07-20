import { useState, type ReactNode } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { Icon } from './Icon'

type NavKey = 'home' | 'diagnosis' | 'records' | 'centers'

interface AppLayoutProps {
  children: ReactNode
  active?: NavKey
  back?: boolean
  className?: string
}

const navItems: Array<[NavKey, string, string, string]> = [
  ['home', 'home', '홈', '/dashboard'],
  ['diagnosis', 'analytics', '진단', '/diagnosis'],
  ['records', 'edit_note', '기록', '/records'],
  ['centers', 'location_on', '센터', '/centers'],
]

export function AppLayout({ children, active, back = false, className = '' }: AppLayoutProps) {
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)
  return (
    <main
      id="main-content"
      className={`relative mx-auto min-h-dvh max-w-[480px] overflow-x-clip bg-background px-5 pb-[calc(7rem+env(safe-area-inset-bottom))] pt-5 text-on-surface md:my-8 md:min-h-[calc(100vh-4rem)] md:rounded-[2.4rem] md:shadow-xl ${className}`}
    >
      <a
        href="#page-content"
        className="sr-only z-50 rounded-full bg-primary px-4 py-2 text-white focus:not-sr-only focus:fixed focus:left-4 focus:top-4"
      >
        본문으로 건너뛰기
      </a>
      <header className="sticky top-0 z-20 -mx-5 mb-7 flex h-14 items-center justify-between border-b border-transparent bg-background/95 px-5 backdrop-blur-xl">
        <button
          type="button"
          className="grid size-11 place-items-center rounded-full text-primary transition hover:bg-primary-container focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          onClick={() => (back ? navigate(-1) : setMenuOpen((open) => !open))}
          aria-label={back ? '뒤로가기' : '메뉴'}
          aria-expanded={!back ? menuOpen : undefined}
          aria-controls={!back ? 'app-menu' : undefined}
        >
          <Icon name={back ? 'arrow_back' : 'menu'} className="text-2xl" />
        </button>
        <NavLink to="/dashboard" className="font-display text-[23px] font-bold tracking-[-.07em] text-primary">
          icecream
        </NavLink>
        <button
          type="button"
          className="relative size-11 rounded-full border-[3px] border-white bg-gradient-to-br from-[#ffe4cf] to-[#8dbba9] text-xl shadow-sm focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          onClick={() => navigate('/onboarding')}
          aria-label="프로필"
        />
        {!back && menuOpen && (
          <div
            id="app-menu"
            className="absolute left-5 top-14 z-30 w-52 rounded-2xl border border-outline-variant/50 bg-white p-2 shadow-xl"
            role="menu"
          >
            <NavLink
              role="menuitem"
              className="flex min-h-11 items-center rounded-xl px-3 text-sm hover:bg-surface-container-low"
              to="/onboarding"
              onClick={() => setMenuOpen(false)}
            >
              <Icon name="face" className="mr-2" />
              아이 프로필
            </NavLink>
            <NavLink
              role="menuitem"
              className="flex min-h-11 items-center rounded-xl px-3 text-sm hover:bg-surface-container-low"
              to="/activities"
              onClick={() => setMenuOpen(false)}
            >
              <Icon name="sports_score" className="mr-2" />
              활동 추천
            </NavLink>
            <NavLink
              role="menuitem"
              className="flex min-h-11 items-center rounded-xl px-3 text-sm hover:bg-surface-container-low"
              to="/regional"
              onClick={() => setMenuOpen(false)}
            >
              <Icon name="map" className="mr-2" />
              지역 인사이트
            </NavLink>
          </div>
        )}
      </header>
      <div id="page-content">{children}</div>
      {active && (
        <nav
          aria-label="주요 메뉴"
          className="fixed bottom-0 left-1/2 z-30 grid min-h-[88px] w-full max-w-[480px] -translate-x-1/2 grid-cols-4 items-center border-t border-outline-variant/30 bg-background/90 px-5 pb-[calc(.75rem+env(safe-area-inset-bottom))] pt-2 backdrop-blur-xl"
        >
          {navItems.map(([key, icon, label, to]) => (
            <NavLink
              key={key}
              to={to}
              className={`flex min-h-16 flex-col items-center justify-center gap-1 rounded-xl font-display text-xs font-semibold transition hover:bg-primary-container/40 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary ${active === key ? 'text-primary' : 'text-on-surface-variant'}`}
            >
              <span
                className={`grid h-9 w-11 place-items-center rounded-full transition duration-200 ${active === key ? 'bg-primary-container' : ''}`}
              >
                <Icon name={icon} className="text-2xl" filled={active === key} />
              </span>
              {label}
            </NavLink>
          ))}
        </nav>
      )}
    </main>
  )
}

export function SectionTitle({ title, action }: { title: string; action?: ReactNode }) {
  return (
    <div className="flex items-center justify-between gap-4">
      <h2 className="font-display text-xl font-bold tracking-[-.07em]">{title}</h2>
      {action}
    </div>
  )
}

export function Card({ children, className = '' }: { children: ReactNode; className?: string }) {
  return (
    <section
      className={`rounded-3xl border border-outline-variant/40 bg-surface-container-lowest shadow-soft ${className}`}
    >
      {children}
    </section>
  )
}

export function GradeBadge({ grade = '새싹', dark = false }: { grade?: string; dark?: boolean }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-4 py-2 font-label ${dark ? 'bg-primary text-white' : 'bg-primary-container text-on-primary-container'}`}
    >
      <Icon name="eco" filled />
      {grade} 등급
    </span>
  )
}
