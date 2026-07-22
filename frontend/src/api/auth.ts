import { apiRequest, setAccessToken, unwrapData } from './client'

export interface Parent {
  id: string
  email: string
  createdAt?: string
}

export interface AuthResult {
  parent: Parent
  accessToken: string
  tokenType: string
}

interface AuthResponse {
  success?: boolean
  data?: AuthResult
}

export async function signup(email: string, password: string) {
  const response = await apiRequest<AuthResponse>('/api/v1/auth/signup', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  const result = unwrapData<AuthResult>(response)
  setAccessToken(result.accessToken)
  return result
}

export async function login(email: string, password: string) {
  const response = await apiRequest<AuthResponse>('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  const result = unwrapData<AuthResult>(response)
  setAccessToken(result.accessToken)
  return result
}

export async function getCurrentParent() {
  const response = await apiRequest<{ data?: Parent }>('/api/v1/auth/me')
  return unwrapData<Parent>(response)
}
