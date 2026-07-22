import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { Icon } from './Icon'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode
  trailingIcon?: string
}

export function PrimaryButton({
  children,
  trailingIcon = 'arrow_forward',
  className = '',
  type = 'button',
  ...props
}: ButtonProps) {
  return (
    <button
      type={type}
      className={`inline-flex min-h-12 items-center justify-center gap-2 rounded-full bg-primary px-6 font-label text-white shadow-mint transition hover:opacity-90 active:scale-[.98] ${className}`}
      {...props}
    >
      {children}
      <Icon name={trailingIcon} />
    </button>
  )
}

export function PillButton({ children, active = false, className = '', ...props }: ButtonProps & { active?: boolean }) {
  return (
    <button
      type="button"
      aria-pressed={active}
      className={`min-h-11 shrink-0 whitespace-nowrap rounded-full border px-4 text-label transition ${active ? 'border-primary bg-primary-container text-on-primary-container' : 'border-outline-variant bg-surface-container-low text-on-surface-variant hover:bg-surface-container'} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
