/**
 * Shopping cart state management with Zustand.
 */
import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { Entity } from '@/types'

interface CartItem {
  entity: Entity
  quantity: number
}

interface CartState {
  items: CartItem[]
  total: number

  // Actions
  addItem: (entity: Entity, quantity?: number) => void
  removeItem: (entityId: number) => void
  updateQuantity: (entityId: number, quantity: number) => void
  clearCart: () => void
  getItemCount: () => number
  calculateTotal: () => number
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      total: 0,

      addItem: (entity: Entity, quantity: number = 1) => {
        const items = get().items
        const existingItem = items.find((item) => item.entity.id === entity.id)

        if (existingItem) {
          // Update quantity
          set({
            items: items.map((item) =>
              item.entity.id === entity.id
                ? { ...item, quantity: item.quantity + quantity }
                : item
            ),
          })
        } else {
          // Add new item
          set({ items: [...items, { entity, quantity }] })
        }

        // Recalculate total
        set({ total: get().calculateTotal() })
      },

      removeItem: (entityId: number) => {
        set({ items: get().items.filter((item) => item.entity.id !== entityId) })
        set({ total: get().calculateTotal() })
      },

      updateQuantity: (entityId: number, quantity: number) => {
        if (quantity <= 0) {
          get().removeItem(entityId)
          return
        }

        set({
          items: get().items.map((item) =>
            item.entity.id === entityId ? { ...item, quantity } : item
          ),
        })
        set({ total: get().calculateTotal() })
      },

      clearCart: () => {
        set({ items: [], total: 0 })
      },

      getItemCount: () => {
        return get().items.reduce((count, item) => count + item.quantity, 0)
      },

      calculateTotal: () => {
        return get().items.reduce(
          (total, item) => total + (item.entity.price || 0) * item.quantity,
          0
        )
      },
    }),
    {
      name: 'cart-storage',
    }
  )
)
