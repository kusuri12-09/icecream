export function Character({ large = false }: { large?: boolean }) {
  return (
    <div
      role="img"
      aria-label="성장 일러스트 영역"
      className={`rounded-full border-4 border-white/70 bg-gradient-to-br from-[#f8ecd9] to-[#e5f3e9] shadow-soft ${large ? 'size-36' : 'size-28'}`}
    />
  )
}
