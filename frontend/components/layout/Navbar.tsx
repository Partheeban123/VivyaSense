'use client'

import { useState } from 'react'
import Link from 'next/link'
import { FaBars, FaTimes, FaVideo } from 'react-icons/fa'

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/detection', label: 'Detection' },
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/analytics', label: 'Analytics' },
    { href: '/contact', label: 'Contact' },
  ]

  return (
    <nav
      className="fixed top-0 w-full bg-white/98 backdrop-blur-md shadow-lg z-50 border-b border-gray-100"
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <Link
            href="/"
            className="flex items-center space-x-3 group"
            aria-label="VivyaSense - Home"
          >
            <div className="p-2 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl group-hover:scale-110 transition-transform">
              <FaVideo className="text-3xl text-white" aria-hidden="true" />
            </div>
            <span className="text-3xl font-extrabold text-gray-900">
              Vivya<span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Sense</span>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-10">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-lg text-gray-700 hover:text-blue-600 font-semibold transition-all hover:scale-105 relative group px-2 py-2"
              >
                {link.label}
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-600 to-purple-600 group-hover:w-full transition-all duration-300" aria-hidden="true"></span>
              </Link>
            ))}
            <Link href="/contact" aria-label="Get started with VivyaSense">
              <button className="min-w-[44px] min-h-[44px] px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-bold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
                Get Started
              </button>
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden text-gray-700 hover:text-blue-600 p-3 min-w-[44px] min-h-[44px]"
            aria-label={isOpen ? "Close navigation menu" : "Open navigation menu"}
            aria-expanded={isOpen}
            aria-controls="mobile-menu"
          >
            {isOpen ? <FaTimes size={28} aria-hidden="true" /> : <FaBars size={28} aria-hidden="true" />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div
          id="mobile-menu"
          className="md:hidden bg-white border-t border-gray-100 shadow-lg"
          role="navigation"
          aria-label="Mobile navigation menu"
        >
          <div className="px-6 pt-4 pb-6 space-y-3">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="block px-6 py-4 text-lg text-gray-700 hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 hover:text-blue-600 rounded-xl transition-all font-semibold min-h-[44px]"
                onClick={() => setIsOpen(false)}
              >
                {link.label}
              </Link>
            ))}
            <Link href="/contact" onClick={() => setIsOpen(false)} aria-label="Get started with VivyaSense">
              <button className="w-full min-h-[44px] px-6 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-bold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg text-lg">
                Get Started
              </button>
            </Link>
          </div>
        </div>
      )}
    </nav>
  )
}

