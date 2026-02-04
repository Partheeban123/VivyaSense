'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { FaVideo, FaExclamationTriangle, FaHardHat, FaFire, FaUserInjured, FaChartLine, FaClock, FaCheckCircle } from 'react-icons/fa'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'

export default function DashboardPage() {
  // Mock data
  const stats = [
    { icon: <FaVideo />, label: 'Active Cameras', value: '12', color: 'blue' },
    { icon: <FaExclamationTriangle />, label: 'Total Alerts', value: '47', color: 'red' },
    { icon: <FaCheckCircle />, label: 'Detections Today', value: '156', color: 'green' },
    { icon: <FaClock />, label: 'Uptime', value: '99.9%', color: 'purple' },
  ]

  const recentDetections = [
    { type: 'PPE Violation', location: 'Warehouse A', time: '2 mins ago', severity: 'high' },
    { type: 'Fall Detected', location: 'Factory Floor', time: '15 mins ago', severity: 'critical' },
    { type: 'Fire Alert', location: 'Storage Room', time: '1 hour ago', severity: 'critical' },
    { type: 'PPE Violation', location: 'Loading Dock', time: '2 hours ago', severity: 'medium' },
  ]

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100">
      <Navbar />

      <div className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Dashboard</h1>
            <p className="text-gray-600">Monitor your AI-powered surveillance system</p>
          </motion.div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
              >
                <div className={`text-3xl text-${stat.color}-600 mb-3`}>
                  {stat.icon}
                </div>
                <p className="text-gray-600 text-sm mb-1">{stat.label}</p>
                <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
              </motion.div>
            ))}
          </div>

          {/* Recent Detections */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-xl shadow-lg p-6 mb-8"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Detections</h2>
            <div className="space-y-4">
              {recentDetections.map((detection, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center space-x-4">
                    <div className={`w-3 h-3 rounded-full ${
                      detection.severity === 'critical' ? 'bg-red-500' :
                      detection.severity === 'high' ? 'bg-orange-500' :
                      'bg-yellow-500'
                    }`}></div>
                    <div>
                      <p className="font-semibold text-gray-900">{detection.type}</p>
                      <p className="text-sm text-gray-600">{detection.location}</p>
                    </div>
                  </div>
                  <p className="text-sm text-gray-500">{detection.time}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            <Link href="/detection" className="block">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 text-white hover:shadow-xl transition-shadow">
                <FaHardHat className="text-4xl mb-3" />
                <h3 className="text-xl font-bold mb-2">Try Detection</h3>
                <p className="text-blue-100">Upload images for instant AI detection</p>
              </div>
            </Link>

            <Link href="/cameras" className="block">
              <div className="bg-gradient-to-r from-green-600 to-teal-600 rounded-xl shadow-lg p-6 text-white hover:shadow-xl transition-shadow">
                <FaVideo className="text-4xl mb-3" />
                <h3 className="text-xl font-bold mb-2">Manage Cameras</h3>
                <p className="text-green-100">Configure and monitor camera feeds</p>
              </div>
            </Link>

            <Link href="/analytics" className="block">
              <div className="bg-gradient-to-r from-orange-600 to-red-600 rounded-xl shadow-lg p-6 text-white hover:shadow-xl transition-shadow">
                <FaChartLine className="text-4xl mb-3" />
                <h3 className="text-xl font-bold mb-2">View Analytics</h3>
                <p className="text-orange-100">Detailed reports and insights</p>
              </div>
            </Link>
          </motion.div>
        </div>
      </div>

      <Footer />
    </main>
  )
}

