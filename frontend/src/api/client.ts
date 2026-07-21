const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000').replace(/\/$/, '')
const ACCESS_TOKEN_KEY = 'icecream.accessToken'

export class ApiError extends Error {
  readonly status: number
  readonly code: string

  constructor(message: string, status: number, code = `HTTP_${status}`) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
  }
}

export function getAccessToken() {
  return window.localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function setAccessToken(token: string) {
  window.localStorage.setItem(ACCESS_TOKEN_KEY, token)
}

export function clearAccessToken() {
  window.localStorage.removeItem(ACCESS_TOKEN_KEY)
}

export async function apiRequest<T>(path: string, init: RequestInit = {}) {
  const headers = new Headers(init.headers)
  if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json')

  const token = getAccessToken()
  if (token) headers.set('Authorization', `Bearer ${token}`)

  const response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers })
  const payload = await readPayload(response)

  if (!response.ok) {
    if (response.status === 401) clearAccessToken()
    const error = isRecord(payload) && isRecord(payload.error) ? payload.error : payload
    const message = isRecord(error) && typeof error.message === 'string' ? error.message : getDetail(payload)
    const code = isRecord(error) && typeof error.code === 'string' ? error.code : `HTTP_${response.status}`
    throw new ApiError(message, response.status, code)
  }

  return payload as T
}

export function unwrapData<T>(payload: unknown): T {
  if (isRecord(payload) && 'data' in payload) return payload.data as T
  return payload as T
}

async function readPayload(response: Response) {
  if (response.status === 204) return null
  const text = await response.text()
  if (!text) return null
  try {
    return JSON.parse(text) as unknown
  } catch {
    return text
  }
}

function getDetail(payload: unknown) {
  if (isRecord(payload) && typeof payload.detail === 'string') return payload.detail
  if (Array.isArray(payload)) return '요청을 처리하지 못했습니다.'
  return '요청을 처리하지 못했습니다.'
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}
