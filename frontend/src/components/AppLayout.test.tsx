import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom'
import { AppLayout } from './AppLayout'

vi.mock('../hooks/useAuth', () => ({
  useAuthActions: () => ({ logout: vi.fn() }),
}))

function Location() {
  return <output data-testid="location">{useLocation().pathname}</output>
}

describe('AppLayout', () => {
  it('하단 탭을 키보드와 클릭으로 이동할 수 있다', () => {
    render(
      <MemoryRouter initialEntries={['/home']}>
        <Routes>
          <Route
            path="*"
            element={
              <>
                <AppLayout active="home">
                  <p>콘텐츠</p>
                </AppLayout>
                <Location />
              </>
            }
          />
        </Routes>
      </MemoryRouter>,
    )

    const recordsLink = screen.getByRole('link', { name: '기록' })
    expect(recordsLink).toHaveAttribute('href', '/records')
    fireEvent.click(recordsLink)
    expect(screen.getByTestId('location')).toHaveTextContent('/records')
  })
})
