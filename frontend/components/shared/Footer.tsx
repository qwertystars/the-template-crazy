import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-gray-50">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
          {/* About */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900">About</h3>
            <p className="mt-4 text-sm text-gray-600">
              FlexiBase is a universal platform framework that transforms
              dynamically through configuration.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900">Quick Links</h3>
            <ul className="mt-4 space-y-2">
              <li>
                <Link
                  href="/products"
                  className="text-sm text-gray-600 hover:text-primary"
                >
                  Products
                </Link>
              </li>
              <li>
                <Link
                  href="/about"
                  className="text-sm text-gray-600 hover:text-primary"
                >
                  About Us
                </Link>
              </li>
              <li>
                <Link
                  href="/contact"
                  className="text-sm text-gray-600 hover:text-primary"
                >
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900">Support</h3>
            <ul className="mt-4 space-y-2">
              <li>
                <Link
                  href="/help"
                  className="text-sm text-gray-600 hover:text-primary"
                >
                  Help Center
                </Link>
              </li>
              <li>
                <Link
                  href="/terms"
                  className="text-sm text-gray-600 hover:text-primary"
                >
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link
                  href="/privacy"
                  className="text-sm text-gray-600 hover:text-primary"
                >
                  Privacy Policy
                </Link>
              </li>
            </ul>
          </div>

          {/* Newsletter */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900">Newsletter</h3>
            <p className="mt-4 text-sm text-gray-600">
              Subscribe to get updates on new features.
            </p>
            <form className="mt-4">
              <input
                type="email"
                placeholder="Enter your email"
                className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-primary focus:outline-none focus:ring-primary"
              />
              <button
                type="submit"
                className="mt-2 w-full rounded-md bg-primary px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary/90"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>

        <div className="mt-8 border-t border-gray-200 pt-8">
          <p className="text-center text-sm text-gray-600">
            © {new Date().getFullYear()} FlexiBase. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
