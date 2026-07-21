import { useQuery, useQueryClient } from '@tanstack/react-query'
import { getCurrentParent, login, signup } from '../api/auth'
import { clearAccessToken, getAccessToken } from '../api/client'

export const useCurrentUser = () =>
  useQuery({
    queryKey: ['auth', 'me'],
    queryFn: getCurrentParent,
    enabled: Boolean(getAccessToken()),
    retry: false,
  })

export function useAuthActions() {
  const queryClient = useQueryClient()

  return {
    login: async (email: string, password: string) => {
      const result = await login(email, password)
      await queryClient.invalidateQueries({ queryKey: ['auth', 'me'] })
      return result
    },
    signup: async (email: string, password: string) => {
      const result = await signup(email, password)
      await queryClient.invalidateQueries({ queryKey: ['auth', 'me'] })
      return result
    },
    logout: () => {
      clearAccessToken()
      queryClient.clear()
    },
  }
}