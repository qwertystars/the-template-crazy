/**
 * Core TypeScript types and interfaces.
 */

// User types
export enum UserRole {
  ADMIN = 'admin',
  CUSTOMER = 'customer',
  DONOR = 'donor',
  SUBSCRIBER = 'subscriber',
  BENEFICIARY = 'beneficiary',
  GUEST = 'guest',
}

export interface User {
  id: number
  email: string
  username?: string
  first_name?: string
  last_name?: string
  phone?: string
  avatar_url?: string
  bio?: string
  role: UserRole
  is_active: boolean
  is_verified: boolean
  is_superuser: boolean
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
  last_login?: string
}

export interface UserCreate {
  email: string
  password: string
  username?: string
  first_name?: string
  last_name?: string
  phone?: string
  bio?: string
  role?: UserRole
}

export interface UserUpdate {
  email?: string
  username?: string
  first_name?: string
  last_name?: string
  phone?: string
  bio?: string
  avatar_url?: string
  metadata?: Record<string, any>
}

export interface UserLogin {
  email: string
  password: string
}

export interface Token {
  access_token: string
  refresh_token?: string
  token_type: string
}

// Entity types
export enum EntityType {
  PRODUCT = 'product',
  CAUSE = 'cause',
  SUBSCRIPTION_TIER = 'subscription_tier',
  RESOURCE = 'resource',
  SERVICE = 'service',
  EVENT = 'event',
}

export enum EntityStatus {
  DRAFT = 'draft',
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  ARCHIVED = 'archived',
}

export interface Entity {
  id: number
  entity_type: EntityType
  status: EntityStatus
  name: string
  slug: string
  description?: string
  short_description?: string
  price?: number
  currency: string
  compare_at_price?: number
  stock_quantity: number
  track_inventory: boolean
  allow_backorder: boolean
  image_url?: string
  gallery?: string[]
  meta_title?: string
  meta_description?: string
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
  published_at?: string
}

export interface EntityCreate {
  entity_type: EntityType
  name: string
  slug: string
  description?: string
  short_description?: string
  price?: number
  currency?: string
  status?: EntityStatus
}

export interface EntityUpdate {
  name?: string
  description?: string
  short_description?: string
  price?: number
  status?: EntityStatus
}

// Transaction types
export enum TransactionType {
  PURCHASE = 'purchase',
  DONATION = 'donation',
  SUBSCRIPTION = 'subscription',
  REFUND = 'refund',
  ALLOCATION = 'allocation',
  PAYMENT = 'payment',
}

export enum TransactionStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled',
  REFUNDED = 'refunded',
}

export interface Transaction {
  id: number
  transaction_type: TransactionType
  status: TransactionStatus
  user_id?: number
  entity_id?: number
  amount: number
  currency: string
  quantity: number
  tax_amount?: number
  discount_amount?: number
  total_amount: number
  payment_method?: string
  payment_gateway?: string
  gateway_transaction_id?: string
  description?: string
  notes?: string
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
  completed_at?: string
}

export interface TransactionCreate {
  transaction_type: TransactionType
  amount: number
  currency?: string
  quantity?: number
  entity_id?: number
  payment_method?: string
  metadata?: Record<string, any>
}

// Platform configuration types
export interface PlatformConfig {
  platformType: string
  platformName: string
  activeModules: string[]
  theme: {
    name: string
    primaryColor: string
    layout: string
  }
  features: Record<string, boolean>
  paymentGateways: string[]
  integrations: Record<string, string>
}

// API response types
export interface ApiError {
  detail: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}
