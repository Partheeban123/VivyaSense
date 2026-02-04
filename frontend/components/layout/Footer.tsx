'use client'

import Link from 'next/link'
import { FaVideo, FaGithub, FaLinkedin, FaTwitter, FaEnvelope } from 'react-icons/fa'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-8 py-16">
        <div className="grid md:grid-cols-4 gap-12">
          {/* Brand */}
          <div>
            <Link href="/" className="flex items-center space-x-3 mb-6 group">
              <div className="p-2 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl group-hover:scale-110 transition-transform">
                <FaVideo className="text-3xl text-white" />
              </div>
              <span className="text-3xl font-extrabold text-white">
                Vivya<span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Sense</span>
              </span>
            </Link>
            <p className="text-base text-gray-400 leading-relaxed mb-6">
              AI-powered video surveillance platform for enterprise security
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-blue-400 transition-colors">
                <FaTwitter size={24} />
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-400 transition-colors">
                <FaLinkedin size={24} />
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-400 transition-colors">
                <FaGithub size={24} />
              </a>
            </div>
          </div>

          {/* Product */}
          <div>
            <h3 className="text-white font-bold text-xl mb-6">Product</h3>
            <ul className="space-y-3">
              <li><Link href="/detection" className="text-base hover:text-blue-400 transition-colors hover:translate-x-1 inline-block">Detection</Link></li>
              <li><Link href="/cameras" className="text-base hover:text-blue-400 transition-colors hover:translate-x-1 inline-block">Cameras</Link></li>
              <li><Link href="/dashboard" className="text-base hover:text-blue-400 transition-colors hover:translate-x-1 inline-block">Dashboard</Link></li>
              <li><Link href="/analytics" className="text-base hover:text-blue-400 transition-colors hover:translate-x-1 inline-block">Analytics</Link></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-white font-bold text-xl mb-6">Company</h3>
            <ul className="space-y-3">
              <li><Link href="/contact" className="text-base hover:text-blue-400 transition-colors hover:translate-x-1 inline-block">About Us</Link></li>
              <li><Link href="/contact" className="text-base hover:text-blue-400 transition-colors hover:translate-x-1 inline-block">Contact</Link></li>
              <li><Link href="/contact" className="text-base hover:text-blue-400 transition-colors hover:translate-x-1 inline-block">Privacy Policy</Link></li>
              <li><Link href="/contact" className="text-base hover:text-blue-400 transition-colors hover:translate-x-1 inline-block">Terms of Service</Link></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white font-bold text-xl mb-6">Get in Touch</h3>
            <p className="text-base text-gray-400 mb-4 leading-relaxed">
              Have questions? We'd love to hear from you.
            </p>
            <Link href="/contact">
              <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-bold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
                Contact Us
              </button>
            </Link>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-12 pt-8 text-center">
          <p className="text-base text-gray-400">&copy; {currentYear} Vivya Sense. All rights reserved. Built with ❤️ for enterprise security.</p>
        </div>
      </div>
    </footer>
  )
}

