'use client'

import { motion } from 'framer-motion'
import { FaChartLine, FaChartBar, FaChartPie, FaDownload } from 'react-icons/fa'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'

export default function AnalyticsPage() {
  const metrics = [
    { label: 'PPE Violations', value: 234, change: '+12%', trend: 'up' },
    { label: 'Fall Incidents', value: 8, change: '-25%', trend: 'down' },
    { label: 'Fire Alerts', value: 3, change: '0%', trend: 'neutral' },
    { label: 'Total Detections', value: 1247, change: '+8%', trend: 'up' },
  ]

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100">
      <Navbar />

      <div className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8 flex justify-between items-center"
          >
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">Analytics & Reports</h1>
              <p className="text-gray-600">Detailed insights from your surveillance system</p>
            </div>
            <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-shadow flex items-center space-x-2">
              <FaDownload />
              <span>Export Report</span>
            </button>
          </motion.div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {metrics.map((metric, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <p className="text-gray-600 text-sm mb-2">{metric.label}</p>
                <p className="text-3xl font-bold text-gray-900 mb-2">{metric.value}</p>
                <p className={`text-sm font-semibold ${
                  metric.trend === 'up' ? 'text-red-600' :
                  metric.trend === 'down' ? 'text-green-600' :
                  'text-gray-600'
                }`}>
                  {metric.change} from last month
                </p>
              </motion.div>
            ))}
          </div>

          {/* Charts Placeholder */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-white rounded-xl shadow-lg p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">Detection Trends</h3>
                <FaChartLine className="text-2xl text-blue-600" />
              </div>
              <div className="h-64 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg flex items-center justify-center">
                <p className="text-gray-500">Chart visualization coming soon</p>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="bg-white rounded-xl shadow-lg p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">Detection Types</h3>
                <FaChartPie className="text-2xl text-purple-600" />
              </div>
              <div className="h-64 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg flex items-center justify-center">
                <p className="text-gray-500">Chart visualization coming soon</p>
              </div>
            </motion.div>
          </div>

          {/* Hourly Activity */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-gray-900">Hourly Activity</h3>
              <FaChartBar className="text-2xl text-green-600" />
            </div>
            <div className="h-64 bg-gradient-to-br from-green-50 to-teal-50 rounded-lg flex items-center justify-center">
              <p className="text-gray-500">Chart visualization coming soon</p>
            </div>
          </motion.div>

          {/* Info Box */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="mt-8 bg-blue-50 border border-blue-200 rounded-xl p-6"
          >
            <h3 className="text-lg font-bold text-blue-900 mb-2">📊 Advanced Analytics</h3>
            <p className="text-blue-800">
              Detailed charts and visualizations will be available once you start processing detections. 
              Try uploading images or connecting cameras to generate analytics data.
            </p>
          </motion.div>
        </div>
      </div>

      <Footer />
    </main>
  )
}

