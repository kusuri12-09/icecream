import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { ErrorState } from './AsyncState'

describe('ErrorState', () => {
  it('다시 시도 버튼으로 조회를 재요청한다', () => {
    const onRetry = vi.fn()
    render(<ErrorState message="조회 실패" onRetry={onRetry} />)

    expect(screen.getByRole('alert')).toHaveTextContent('조회 실패')
    fireEvent.click(screen.getByRole('button', { name: '다시 시도' }))
    expect(onRetry).toHaveBeenCalledOnce()
  })
})
