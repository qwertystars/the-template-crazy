/**
 * Authentication state management with Zustand.
 */
import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import api from '@/lib/api'
import { User, UserLogin, Token } from '@/types'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  // Actions
  login: (credentials: UserLogin) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
  fetchCurrentUser: () => Promise<void>
  clearError: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (credentials: UserLogin) => {
        set({ isLoading: true, error: null })

        try {
          const response = await api.post<Token>('/v1/auth/login', credentials)
          const { access_token, refresh_token } = response.data

          // Store tokens
          localStorage.setItem('access_token', access_token)
          if (refresh_token) {
            localStorage.setItem('refresh_token', refresh_token)
          }

          set({ token: access_token, isAuthenticated: true })

          // Fetch user profile
          await get().fetchCurrentUser()
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 'Login failed'
          set({ error: errorMessage, isAuthenticated: false })
          throw error
        } finally {
          set({ isLoading: false })
        }
      },

      logout: () => {
        // Clear tokens
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')

        set({
          user: null,
          token: null,
          isAuthenticated: false,
          error: null,
        })
      },

      setUser: (user: User) => {
        set({ user })
      },

      fetchCurrentUser: async () => {
        try {
          const response = await api.get<User>('/v1/users/me')
          set({ user: response.data, isAuthenticated: true })
        } catch (error: any) {
          const errorMessage = error.response?.data?.detail || 'Failed to fetch user'
          set({ error: errorMessage })
          throw error
        }
      },

      clearError: () => {
        set({ error: null })
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
