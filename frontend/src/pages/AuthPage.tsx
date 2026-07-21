import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ApiError } from '../api/client'
import { useAuthActions } from '../hooks/useAuth'

export function AuthPage({ mode }: { mode: 'login' | 'signup' }) {
  const navigate = useNavigate()
  const { login, signup } = useAuthActions()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const isSignup = mode === 'signup'

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    if (!email.trim() || !password) {
      setError('이메일과 비밀번호를 입력해주세요.')
      return
    }
    if (isSignup && (password.length < 8 || password.length > 64)) {
      setError('비밀번호는 8~64자로 입력해주세요.')
      return
    }

    setSubmitting(true)
    try {
      if (isSignup) {
        await signup(email.trim(), password)
        navigate('/onboarding', { replace: true })
      } else {
        await login(email.trim(), password)
        navigate('/dashboard', { replace: true })
      }
    } catch (cause) {
      setError(cause instanceof ApiError ? cause.message : '요청을 처리하지 못했습니다. 잠시 후 다시 시도해주세요.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="grid min-h-dvh place-items-center bg-background px-5 py-10 text-on-surface">
      <section className="w-full max-w-[420px] rounded-[2rem] border border-outline-variant/40 bg-white p-7 shadow-soft">
        <p className="font-display text-2xl font-bold tracking-[-.07em] text-primary">icecream</p>
        <h1 className="mt-10 font-display text-[28px] font-bold tracking-[-.08em]">
          {isSignup ? '아이의 성장을 시작해요' : '다시 만나서 반가워요'}
        </h1>
        <p className="mt-3 text-sm leading-6 text-on-surface-variant">
          {isSignup ? '학부모 계정을 만들고 성장 기록을 시작해보세요.' : '로그인하고 우리 아이의 성장 기록을 확인해보세요.'}
        </p>
        <form className="mt-8 grid gap-4" onSubmit={handleSubmit}>
          <label className="grid gap-2 text-sm font-semibold">
            이메일
            <input
              type="email"
              autoComplete="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="h-[52px] rounded-full border border-outline-variant/50 bg-[#fffdf5] px-5 font-normal outline-none focus:border-primary focus:ring-4 focus:ring-primary-container/50"
              placeholder="parent@example.com"
            />
          </label>
          <label className="grid gap-2 text-sm font-semibold">
            비밀번호
            <input
              type="password"
              autoComplete={isSignup ? 'new-password' : 'current-password'}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="h-[52px] rounded-full border border-outline-variant/50 bg-[#fffdf5] px-5 font-normal outline-none focus:border-primary focus:ring-4 focus:ring-primary-container/50"
              placeholder={isSignup ? '8~64자' : '비밀번호'}
            />
          </label>
          {error && <p className="rounded-2xl bg-error-container px-4 py-3 text-sm text-on-error-container">{error}</p>}
          <button
            type="submit"
            disabled={submitting}
            className="mt-2 min-h-12 rounded-full bg-primary px-6 font-semibold text-white transition hover:opacity-90 disabled:cursor-wait disabled:opacity-60"
          >
            {submitting ? '처리하고 있어요…' : isSignup ? '회원가입' : '로그인'}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-on-surface-variant">
          {isSignup ? '이미 계정이 있나요?' : '아직 계정이 없나요?'}{' '}
          <Link className="font-semibold text-primary underline underline-offset-4" to={isSignup ? '/login' : '/signup'}>
            {isSignup ? '로그인' : '회원가입'}
          </Link>
        </p>
      </section>
    </main>
  )
}