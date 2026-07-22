import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom'
import { AuthPage } from './AuthPage'

const authMocks = vi.hoisted(() => ({
  login: vi.fn().mockResolvedValue(undefined),
  signup: vi.fn().mockResolvedValue(undefined),
}))

vi.mock('../hooks/useAuth', () => ({
  useAuthActions: () => authMocks,
}))

function Location() {
  return <output data-testid="location">{useLocation().pathname}</output>
}

describe('AuthPage', () => {
  it('로그인 폼 제출 후 대시보드로 이동한다', async () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <Routes>
          <Route
            path="*"
            element={
              <>
                <AuthPage mode="login" />
                <Location />
              </>
            }
          />
        </Routes>
      </MemoryRouter>,
    )

    fireEvent.change(screen.getByLabelText('이메일'), { target: { value: 'parent@example.com' } })
    fireEvent.change(screen.getByLabelText('비밀번호'), { target: { value: 'password123' } })
    fireEvent.click(screen.getByRole('button', { name: '로그인' }))

    await waitFor(() => expect(authMocks.login).toHaveBeenCalledWith('parent@example.com', 'password123'))
    await waitFor(() => expect(screen.getByTestId('location')).toHaveTextContent('/dashboard'))
  })

  it('필수 입력이 없으면 오류를 알리고 제출하지 않는다', () => {
    authMocks.login.mockClear()
    render(
      <MemoryRouter>
        <AuthPage mode="login" />
      </MemoryRouter>,
    )

    fireEvent.click(screen.getByRole('button', { name: '로그인' }))

    expect(screen.getByRole('alert')).toHaveTextContent('이메일과 비밀번호를 입력해주세요.')
    expect(authMocks.login).not.toHaveBeenCalled()
  })
})
