import type { ReactNode } from 'react'

export function LoadingState({ message = '불러오고 있어요…' }: { message?: string }) {
  return (
    <p className="grid min-h-32 place-items-center text-sm text-on-surface-variant" role="status">
      {message}
    </p>
  )
}

export function ErrorState({
  message = '정보를 불러오지 못했어요.',
  onRetry,
}: {
  message?: string
  onRetry?: () => void
}) {
  return (
    <div
      className="grid gap-3 rounded-2xl bg-error-container px-4 py-4 text-center text-sm text-on-error-container"
      role="alert"
    >
      <p>{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mx-auto rounded-full bg-white px-4 py-2 font-semibold text-error"
        >
          다시 시도
        </button>
      )}
    </div>
  )
}

export function EmptyState({ message, action }: { message: string; action?: ReactNode }) {
  return (
    <div className="grid min-h-32 place-items-center gap-3 py-6 text-center text-sm text-on-surface-variant">
      <p>{message}</p>
      {action}
    </div>
  )
}
