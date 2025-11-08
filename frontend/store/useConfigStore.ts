/**
 * Platform configuration state management with Zustand.
 */
import { create } from 'zustand'
import api from '@/lib/api'
import { PlatformConfig } from '@/types'

interface ConfigState {
  config: PlatformConfig | null
  isLoading: boolean
  error: string | null

  // Actions
  fetchConfig: () => Promise<void>
  updateConfig: (config: Partial<PlatformConfig>) => void
  isModuleActive: (moduleName: string) => boolean
}

const defaultConfig: PlatformConfig = {
  platformType: 'ecommerce',
  platformName: 'FlexiBase',
  activeModules: ['commerce', 'reviews'],
  theme: {
    name: 'modern-shop',
    primaryColor: '#3B82F6',
    layout: 'grid',
  },
  features: {
    userRegistration: true,
    guestCheckout: true,
    multiCurrency: false,
    socialLogin: false,
  },
  paymentGateways: ['stripe'],
  integrations: {
    analytics: 'google',
    email: 'sendgrid',
  },
}

export const useConfigStore = create<ConfigState>((set, get) => ({
  config: defaultConfig,
  isLoading: false,
  error: null,

  fetchConfig: async () => {
    set({ isLoading: true, error: null })

    try {
      // TODO: Implement config endpoint in backend
      // For now, use default config
      // const response = await api.get<PlatformConfig>('/v1/config')
      // set({ config: response.data })

      set({ config: defaultConfig })
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to fetch config'
      set({ error: errorMessage })
    } finally {
      set({ isLoading: false })
    }
  },

  updateConfig: (newConfig: Partial<PlatformConfig>) => {
    const currentConfig = get().config
    if (currentConfig) {
      set({ config: { ...currentConfig, ...newConfig } })
    }
  },

  isModuleActive: (moduleName: string) => {
    const config = get().config
    return config?.activeModules.includes(moduleName) || false
  },
}))
