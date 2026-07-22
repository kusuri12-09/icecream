import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { DashboardPage } from './MainPages'

const queryMocks = vi.hoisted(() => ({
  child: {
    data: undefined,
    isLoading: false,
    error: new Error('network failure'),
    refetch: vi.fn(),
  },
}))

vi.mock('../hooks/useAuth', () => ({
  useAuthActions: () => ({ logout: vi.fn() }),
}))

vi.mock('../hooks/useFitnessData', () => ({
  useChild: () => queryMocks.child,
  useRegionalInsight: () => ({ data: undefined }),
  useRegionalMap: () => ({ data: [] }),
  useSaveChild: () => ({ mutateAsync: vi.fn(), isPending: false }),
}))

describe('DashboardPage', () => {
  it('React Query 오류와 재시도 동작을 표시한다', () => {
    render(
      <MemoryRouter>
        <DashboardPage />
      </MemoryRouter>,
    )

    expect(screen.getByRole('alert')).toHaveTextContent('자녀 정보를 불러오지 못했어요.')
    fireEvent.click(screen.getByRole('button', { name: '다시 시도' }))
    expect(queryMocks.child.refetch).toHaveBeenCalledOnce()
  })
})
