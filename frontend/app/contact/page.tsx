'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaEnvelope, FaPhone, FaMapMarkerAlt, FaPaperPlane, FaCheckCircle } from 'react-icons/fa'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Validation helper functions
const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const validatePhone = (phone: string): boolean => {
  if (!phone) return true // Phone is optional
  const cleaned = phone.replace(/[\s\-\(\)\+\.]/g, '')
  return cleaned.length >= 10
}

const validateName = (name: string): boolean => {
  return name.trim().length >= 2 && /^[a-zA-Z\s\-'.]+$/.test(name)
}

const validateMessage = (message: string): boolean => {
  return message.trim().length >= 10 && message.trim().length <= 2000
}

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    phone: '',
    subject: '',
    message: ''
  })
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [apiError, setApiError] = useState<string>('')
  const [rateLimitInfo, setRateLimitInfo] = useState<{
    isLimited: boolean
    retryAfter?: number
  }>({ isLimited: false })

  useEffect(() => {
    console.log('✅ Contact page component mounted - JavaScript is working!')

    // Check rate limit status on mount
    checkRateLimitStatus()
  }, [])

  const checkRateLimitStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/api/contact/stats`)
      if (response.ok) {
        const data = await response.json()
        setRateLimitInfo({
          isLimited: data.is_rate_limited,
          retryAfter: data.seconds_until_reset
        })
      }
    } catch (error) {
      console.error('Failed to check rate limit status:', error)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target

    setFormData({
      ...formData,
      [name]: value
    })

    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: ''
      })
    }

    // Clear API error when user makes changes
    if (apiError) {
      setApiError('')
    }

    // Real-time validation
    let error = ''

    switch (name) {
      case 'name':
        if (value && !validateName(value)) {
          error = 'Name should only contain letters, spaces, hyphens, and apostrophes'
        } else if (value && value.trim().length < 2) {
          error = 'Name must be at least 2 characters'
        }
        break

      case 'email':
        if (value && !validateEmail(value)) {
          error = 'Please enter a valid email address'
        }
        break

      case 'phone':
        if (value && !validatePhone(value)) {
          error = 'Phone number must be at least 10 digits'
        }
        break

      case 'message':
        if (value && value.trim().length < 10) {
          error = 'Message must be at least 10 characters'
        } else if (value && value.trim().length > 2000) {
          error = 'Message must not exceed 2000 characters'
        }
        break
    }

    if (error) {
      setErrors({
        ...errors,
        [name]: error
      })
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    // Required fields
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required'
    } else if (!validateName(formData.name)) {
      newErrors.name = 'Name contains invalid characters'
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }

    if (!formData.subject) {
      newErrors.subject = 'Please select a subject'
    }

    if (!formData.message.trim()) {
      newErrors.message = 'Message is required'
    } else if (!validateMessage(formData.message)) {
      newErrors.message = 'Message must be between 10 and 2000 characters'
    }

    // Optional fields validation
    if (formData.phone && !validatePhone(formData.phone)) {
      newErrors.phone = 'Please enter a valid phone number'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    console.log('🎯 handleSubmit CALLED!')
    e.preventDefault()

    // Clear previous errors
    setApiError('')

    // Validate form
    if (!validateForm()) {
      console.log('❌ Form validation failed')
      return
    }

    // Check rate limit
    if (rateLimitInfo.isLimited) {
      const minutes = Math.ceil((rateLimitInfo.retryAfter || 0) / 60)
      setApiError(`You've reached the submission limit. Please try again in ${minutes} minute${minutes > 1 ? 's' : ''}.`)
      return
    }

    console.log('🚀 Form submission started')
    console.log('📋 Form data:', formData)
    setLoading(true)

    try {
      console.log(`📤 Sending request to: ${API_URL}/api/contact`)

      // Call backend API
      const response = await fetch(`${API_URL}/api/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      console.log('📥 Response received:', response.status, response.statusText)

      const result = await response.json()
      console.log('📦 Response data:', result)

      if (!response.ok) {
        // Handle different error types
        if (response.status === 429) {
          // Rate limit exceeded
          const retryAfter = result.detail?.retry_after || 3600
          const minutes = Math.ceil(retryAfter / 60)
          setApiError(`Too many submissions. Please try again in ${minutes} minute${minutes > 1 ? 's' : ''}.`)
          setRateLimitInfo({
            isLimited: true,
            retryAfter: retryAfter
          })
        } else if (response.status === 400) {
          // Validation error
          const errorMessage = result.detail?.message || result.detail || 'Please check your input and try again.'
          setApiError(errorMessage)
        } else if (response.status === 500) {
          // Server error
          setApiError('Server error. Please try again later or contact support.')
        } else {
          // Other errors
          setApiError(`Failed to submit form: ${result.detail?.message || response.statusText}`)
        }

        setLoading(false)
        return
      }

      console.log('✅ Contact form submitted successfully:', result)

      setLoading(false)
      setSubmitted(true)

      // Update rate limit info
      await checkRateLimitStatus()

      // Reset form after 5 seconds
      setTimeout(() => {
        setSubmitted(false)
        setFormData({
          name: '',
          email: '',
          company: '',
          phone: '',
          subject: '',
          message: ''
        })
        setErrors({})
      }, 5000)

    } catch (error) {
      console.error('❌ Error submitting contact form:', error)
      console.error('❌ Error details:', error instanceof Error ? error.message : String(error))
      setLoading(false)

      // Network error or other unexpected error
      if (error instanceof TypeError && error.message.includes('fetch')) {
        setApiError('Network error. Please check your connection and try again.')
      } else {
        setApiError('An unexpected error occurred. Please try again later.')
      }
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100">
      <Navbar />
      
      <div className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <h1 className="text-6xl md:text-7xl font-extrabold text-gray-900 mb-6">
              Get in <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">Touch</span>
            </h1>
            <p className="text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Have questions about Vivya Sense? We're here to help you transform your security infrastructure.
            </p>
          </motion.div>

          <div className="grid lg:grid-cols-3 gap-10">
            {/* Contact Info */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="lg:col-span-1 space-y-8"
            >
              <div className="bg-white rounded-2xl p-8 shadow-xl">
                <h3 className="text-3xl font-bold text-gray-900 mb-8">Contact Information</h3>
                
                <div className="space-y-6">
                  <div className="flex items-start space-x-4">
                    <div className="p-3 bg-blue-100 rounded-xl" aria-hidden="true">
                      <FaEnvelope className="text-2xl text-blue-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-700 mb-1">Email</p>
                      <a href="mailto:contact@vivyasense.com" className="text-base font-semibold text-gray-900 hover:text-blue-600 transition-colors">
                        contact@vivyasense.com
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="p-3 bg-purple-100 rounded-xl" aria-hidden="true">
                      <FaPhone className="text-2xl text-purple-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-700 mb-1">Phone</p>
                      <a href="tel:+918807708080" className="text-base font-semibold text-gray-900 hover:text-purple-600 transition-colors">
                        +91 880 770 8080
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="p-3 bg-pink-100 rounded-xl" aria-hidden="true">
                      <FaMapMarkerAlt className="text-2xl text-pink-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-700 mb-1">Address</p>
                      <a
                        href="https://www.google.com/maps/search/?api=1&query=B2+B-Block+Greenwoods+Morais+City+Sembattu+Tiruchirappalli+Airport+Tiruchirappalli+620007+Tamil+Nadu+India"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-base font-semibold text-gray-900 hover:text-pink-600 transition-colors cursor-pointer block"
                      >
                        <address className="not-italic leading-relaxed">
                          B2, B-Block, Greenwoods, Morais City<br />
                          Sembattu, Tiruchirappalli Airport<br />
                          Tiruchirappalli - 620007, Tamil Nadu<br />
                          India
                        </address>
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-2xl p-8 text-white shadow-xl">
                <h4 className="text-2xl font-bold mb-4">Why Choose Vivya Sense?</h4>
                <ul className="space-y-3 text-white/90">
                  <li className="flex items-center space-x-2">
                    <FaCheckCircle className="text-xl" />
                    <span>Real-time AI detection</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <FaCheckCircle className="text-xl" />
                    <span>Enterprise-grade security</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <FaCheckCircle className="text-xl" />
                    <span>24/7 Support</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <FaCheckCircle className="text-xl" />
                    <span>Easy integration</span>
                  </li>
                </ul>
              </div>
            </motion.div>

            {/* Contact Form */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className="lg:col-span-2"
            >
              <div className="bg-white rounded-2xl p-10 shadow-xl">
                {submitted ? (
                  <div className="text-center py-16">
                    <div className="inline-block p-6 bg-green-100 rounded-full mb-6">
                      <FaCheckCircle className="text-6xl text-green-600" />
                    </div>
                    <h3 className="text-4xl font-bold text-gray-900 mb-4">Thank You!</h3>
                    <p className="text-xl text-gray-600">
                      We've received your message and will get back to you within 24 hours.
                    </p>
                  </div>
                ) : (
                  <>
                    {/* Rate Limit Warning */}
                    {rateLimitInfo.isLimited && (
                      <div className="mb-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-lg">
                        <div className="flex items-center">
                          <div className="flex-shrink-0">
                            <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                          </div>
                          <div className="ml-3">
                            <p className="text-sm text-yellow-700">
                              You've reached the submission limit. Please try again in {Math.ceil((rateLimitInfo.retryAfter || 0) / 60)} minutes.
                            </p>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* API Error Message */}
                    {apiError && (
                      <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-400 rounded-lg">
                        <div className="flex items-center">
                          <div className="flex-shrink-0">
                            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                          </div>
                          <div className="ml-3">
                            <p className="text-sm text-red-700">{apiError}</p>
                          </div>
                        </div>
                      </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-6" aria-label="Contact form">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="name" className="block text-lg font-semibold text-gray-900 mb-3">
                          Full Name <span aria-label="required">*</span>
                        </label>
                        <input
                          type="text"
                          id="name"
                          name="name"
                          value={formData.name}
                          onChange={handleChange}
                          required
                          aria-required="true"
                          aria-invalid={errors.name ? "true" : "false"}
                          aria-describedby={errors.name ? "name-error" : undefined}
                          className={`w-full px-6 py-4 text-lg border-2 rounded-xl focus:outline-none transition-colors ${
                            errors.name
                              ? 'border-red-400 focus:border-red-600'
                              : 'border-gray-200 focus:border-blue-600'
                          }`}
                          placeholder="John Doe"
                        />
                        {errors.name && (
                          <p id="name-error" role="alert" className="mt-2 text-sm text-red-600">{errors.name}</p>
                        )}
                      </div>

                      <div>
                        <label htmlFor="email" className="block text-lg font-semibold text-gray-900 mb-3">
                          Email Address <span aria-label="required">*</span>
                        </label>
                        <input
                          type="email"
                          id="email"
                          name="email"
                          value={formData.email}
                          onChange={handleChange}
                          required
                          aria-required="true"
                          aria-invalid={errors.email ? "true" : "false"}
                          aria-describedby={errors.email ? "email-error" : undefined}
                          className={`w-full px-6 py-4 text-lg border-2 rounded-xl focus:outline-none transition-colors ${
                            errors.email
                              ? 'border-red-400 focus:border-red-600'
                              : 'border-gray-200 focus:border-blue-600'
                          }`}
                          placeholder="john@company.com"
                        />
                        {errors.email && (
                          <p id="email-error" role="alert" className="mt-2 text-sm text-red-600">{errors.email}</p>
                        )}
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="company" className="block text-lg font-semibold text-gray-900 mb-3">
                          Company
                        </label>
                        <input
                          type="text"
                          id="company"
                          name="company"
                          value={formData.company}
                          onChange={handleChange}
                          className="w-full px-6 py-4 text-lg border-2 border-gray-200 rounded-xl focus:border-blue-600 focus:outline-none transition-colors"
                          placeholder="Your Company"
                        />
                      </div>

                      <div>
                        <label htmlFor="phone" className="block text-lg font-semibold text-gray-900 mb-3">
                          Phone Number
                        </label>
                        <input
                          type="tel"
                          id="phone"
                          name="phone"
                          value={formData.phone}
                          onChange={handleChange}
                          className={`w-full px-6 py-4 text-lg border-2 rounded-xl focus:outline-none transition-colors ${
                            errors.phone
                              ? 'border-red-400 focus:border-red-600'
                              : 'border-gray-200 focus:border-blue-600'
                          }`}
                          placeholder="+91 880 770 8080"
                        />
                        {errors.phone && (
                          <p id="phone-error" role="alert" className="mt-2 text-sm text-red-600">{errors.phone}</p>
                        )}
                      </div>
                    </div>

                    <div>
                      <label htmlFor="subject" className="block text-lg font-semibold text-gray-900 mb-3">
                        Subject <span aria-label="required">*</span>
                      </label>
                      <select
                        id="subject"
                        name="subject"
                        value={formData.subject}
                        onChange={handleChange}
                        required
                        aria-required="true"
                        aria-invalid={errors.subject ? "true" : "false"}
                        aria-describedby={errors.subject ? "subject-error" : undefined}
                        className={`w-full px-6 py-4 text-lg border-2 rounded-xl focus:outline-none transition-colors ${
                          errors.subject
                            ? 'border-red-400 focus:border-red-600'
                            : 'border-gray-200 focus:border-blue-600'
                        }`}
                      >
                        <option value="">Select a subject</option>
                        <option value="Request a Demo">Request a Demo</option>
                        <option value="Pricing Inquiry">Pricing Inquiry</option>
                        <option value="Technical Support">Technical Support</option>
                        <option value="Partnership Opportunity">Partnership Opportunity</option>
                        <option value="Other">Other</option>
                      </select>
                      {errors.subject && (
                        <p id="subject-error" role="alert" className="mt-2 text-sm text-red-600">{errors.subject}</p>
                      )}
                    </div>

                    <div>
                      <label htmlFor="message" className="block text-lg font-semibold text-gray-900 mb-3">
                        Message <span aria-label="required">*</span> <span className="text-sm text-gray-600">({formData.message.length}/2000)</span>
                      </label>
                      <textarea
                        id="message"
                        name="message"
                        value={formData.message}
                        onChange={handleChange}
                        required
                        aria-required="true"
                        aria-invalid={errors.message ? "true" : "false"}
                        aria-describedby={errors.message ? "message-error" : "message-hint"}
                        rows={6}
                        className={`w-full px-6 py-4 text-lg border-2 rounded-xl focus:outline-none transition-colors resize-none ${
                          errors.message
                            ? 'border-red-400 focus:border-red-600'
                            : 'border-gray-200 focus:border-blue-600'
                        }`}
                        placeholder="Tell us about your requirements..."
                      />
                      <p id="message-hint" className="sr-only">Message must be between 10 and 2000 characters</p>
                      {errors.message && (
                        <p id="message-error" role="alert" className="mt-2 text-sm text-red-600">{errors.message}</p>
                      )}
                    </div>

                    <button
                      type="submit"
                      disabled={loading || rateLimitInfo.isLimited}
                      aria-label={loading ? "Sending message" : "Send message"}
                      className="w-full min-h-[44px] px-10 py-5 text-xl bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white rounded-xl font-bold hover:from-blue-700 hover:via-purple-700 hover:to-pink-700 transition-all shadow-2xl hover:shadow-3xl transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-3"
                    >
                      {loading ? (
                        <>
                          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white" aria-hidden="true"></div>
                          <span>Sending...</span>
                        </>
                      ) : rateLimitInfo.isLimited ? (
                        <>
                          <span>Rate Limit Reached</span>
                        </>
                      ) : (
                        <>
                          <FaPaperPlane />
                          <span>Send Message</span>
                        </>
                      )}
                    </button>
                  </form>
                  </>
                )}
              </div>
            </motion.div>
          </div>
        </div>
      </div>

      <Footer />
    </main>
  )
}


