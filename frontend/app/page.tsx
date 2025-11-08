import Link from 'next/link'

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-16">
      <div className="text-center">
        <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl">
          Welcome to{' '}
          <span className="text-primary">FlexiBase</span>
        </h1>
        <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto">
          A modular, full-stack web platform that can be dynamically configured
          to transform into different types of websites through configuration
          changes, without modifying core codebase.
        </p>

        <div className="mt-10 flex items-center justify-center gap-x-6">
          <Link
            href="/products"
            className="rounded-md bg-primary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            Browse Products
          </Link>
          <Link
            href="/login"
            className="text-sm font-semibold leading-6 text-gray-900"
          >
            Sign in <span aria-hidden="true">→</span>
          </Link>
        </div>
      </div>

      <div className="mt-20 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900">
            E-Commerce
          </h3>
          <p className="mt-2 text-sm text-gray-600">
            Full-featured online store with inventory management, shopping cart,
            and checkout.
          </p>
        </div>

        <div className="rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900">
            Donation Platform
          </h3>
          <p className="mt-2 text-sm text-gray-600">
            Fundraising campaigns with goal tracking and impact reporting.
          </p>
        </div>

        <div className="rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900">
            Subscription Service
          </h3>
          <p className="mt-2 text-sm text-gray-600">
            Recurring billing with tier management and access control.
          </p>
        </div>
      </div>
    </div>
  )
}
