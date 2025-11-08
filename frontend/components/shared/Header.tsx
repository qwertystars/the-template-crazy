'use client'

import Link from 'next/link'
import { useAuthStore } from '@/store/useAuthStore'
import { useCartStore } from '@/store/useCartStore'

export default function Header() {
  const { isAuthenticated, user, logout } = useAuthStore()
  const { getItemCount } = useCartStore()

  const handleLogout = () => {
    logout()
  }

  return (
    <header className="border-b border-gray-200 bg-white">
      <nav className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold text-primary">
              FlexiBase
            </Link>
          </div>

          {/* Navigation */}
          <div className="hidden md:flex md:space-x-8">
            <Link
              href="/products"
              className="text-sm font-medium text-gray-700 hover:text-primary"
            >
              Products
            </Link>
            <Link
              href="/about"
              className="text-sm font-medium text-gray-700 hover:text-primary"
            >
              About
            </Link>
            <Link
              href="/contact"
              className="text-sm font-medium text-gray-700 hover:text-primary"
            >
              Contact
            </Link>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-4">
            {/* Cart */}
            <Link
              href="/cart"
              className="relative text-gray-700 hover:text-primary"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
              {getItemCount() > 0 && (
                <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-primary text-xs text-white">
                  {getItemCount()}
                </span>
              )}
            </Link>

            {/* User menu */}
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <Link
                  href="/profile"
                  className="text-sm font-medium text-gray-700 hover:text-primary"
                >
                  {user?.first_name || user?.email}
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-sm font-medium text-gray-700 hover:text-primary"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link
                  href="/login"
                  className="text-sm font-medium text-gray-700 hover:text-primary"
                >
                  Sign in
                </Link>
                <Link
                  href="/register"
                  className="rounded-md bg-primary px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary/90"
                >
                  Sign up
                </Link>
              </div>
            )}
          </div>
        </div>
      </nav>
    </header>
  )
}
