'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'
import { FaVideo, FaPlus, FaPlay, FaStop, FaCamera, FaCheckCircle, FaTimesCircle, FaExclamationTriangle, FaTimes, FaEye, FaEyeSlash } from 'react-icons/fa'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function CamerasPage() {
  // Start with empty cameras array - will be populated when user adds cameras
  const [cameras, setCameras] = useState<any[]>([
    // Example cameras (remove these in production)
    // { id: 1, name: 'Warehouse A - Main', status: 'active', location: 'Building A', fps: 30, rtspUrl: 'rtsp://example.com/stream1', type: 'RTSP' },
    // { id: 2, name: 'Factory Floor - North', status: 'active', location: 'Building B', fps: 30, rtspUrl: 'rtsp://example.com/stream2', type: 'RTSP' },
  ])
  const [showAddModal, setShowAddModal] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [activeStreams, setActiveStreams] = useState<{[key: string]: WebSocket}>({})
  const [streamFrames, setStreamFrames] = useState<{[key: string]: string}>({})
  const [detectionAlerts, setDetectionAlerts] = useState<{[key: string]: any[]}>({})
  const [streamFps, setStreamFps] = useState<{[key: string]: number}>({})
  const [fullscreenCamera, setFullscreenCamera] = useState<number | null>(null)

  // Start camera stream
  const startCameraStream = (camera: any) => {
    const streamId = `camera_${camera.id}`
    const wsUrl = API_URL.replace('http', 'ws') + `/ws/stream/${streamId}`

    try {
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        console.log(`WebSocket connected for camera ${camera.id}`)
        console.log('Detection types:', camera.detectionTypes)
        console.log('Confidence threshold:', camera.confidenceThreshold)

        // Send start command with RTSP URL and detection settings
        ws.send(JSON.stringify({
          action: 'start',
          stream_url: camera.rtspUrl,
          detection_types: camera.detectionTypes || ['ppe', 'fall', 'fire'],
          confidence: camera.confidenceThreshold || 0.5
        }))

        // Update camera status
        setCameras(prev => prev.map(c =>
          c.id === camera.id ? { ...c, status: 'active' } : c
        ))
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)

          if (data.type === 'frame' && data.frame) {
            // Update frame for this camera
            setStreamFrames(prev => ({
              ...prev,
              [camera.id]: `data:image/jpeg;base64,${data.frame}`
            }))

            // Update FPS if present
            if (data.fps) {
              setStreamFps(prev => ({
                ...prev,
                [camera.id]: data.fps
              }))
            }

            // Update detection alerts if present
            if (data.detections && data.detections.length > 0) {
              setDetectionAlerts(prev => ({
                ...prev,
                [camera.id]: data.detections
              }))

              // Log critical alerts
              if (data.has_alerts) {
                const alertTypes = data.detections
                  .filter((d: any) => d.alert)
                  .map((d: any) => d.type)
                  .join(', ')
                console.warn(`🚨 ALERT on ${camera.name}: ${alertTypes}`)
              }
            } else {
              // Clear alerts if no detections
              setDetectionAlerts(prev => ({
                ...prev,
                [camera.id]: []
              }))
            }
          } else if (data.type === 'status') {
            console.log(`Stream status: ${data.message}`)
          } else if (data.type === 'error') {
            console.error(`Stream error: ${data.message}`)
            setCameras(prev => prev.map(c =>
              c.id === camera.id ? { ...c, status: 'error' } : c
            ))
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      ws.onerror = (error) => {
        console.error(`WebSocket error for camera ${camera.id}:`, error)
        setCameras(prev => prev.map(c =>
          c.id === camera.id ? { ...c, status: 'error' } : c
        ))
      }

      ws.onclose = () => {
        console.log(`WebSocket closed for camera ${camera.id}`)
        setActiveStreams(prev => {
          const newStreams = { ...prev }
          delete newStreams[camera.id]
          return newStreams
        })
        setStreamFrames(prev => {
          const newFrames = { ...prev }
          delete newFrames[camera.id]
          return newFrames
        })
      }

      setActiveStreams(prev => ({ ...prev, [camera.id]: ws }))
    } catch (error) {
      console.error(`Failed to start stream for camera ${camera.id}:`, error)
      alert('Failed to start camera stream. Please check the RTSP URL and network connection.')
    }
  }

  // Stop camera stream
  const stopCameraStream = (camera: any) => {
    const ws = activeStreams[camera.id]
    if (ws) {
      ws.send(JSON.stringify({ action: 'stop' }))
      ws.close()

      setCameras(prev => prev.map(c =>
        c.id === camera.id ? { ...c, status: 'inactive' } : c
      ))
    }
  }

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    cameraType: 'rtsp',
    ipAddress: '',
    port: '554',
    username: '',
    password: '',
    streamPath: '/cam/realmonitor?channel=1&subtype=1',
    location: '',
    detectionTypes: [] as string[],
    confidenceThreshold: 0.5,
    alertEnabled: true,
  })

  // Generate RTSP URL from form fields
  const generateRtspUrl = () => {
    if (formData.cameraType === 'rtsp' && formData.ipAddress) {
      const auth = formData.username && formData.password
        ? `${formData.username}:${formData.password}@`
        : ''

      // Clean IP address - remove any protocol prefix
      let cleanIp = formData.ipAddress.trim()
      cleanIp = cleanIp.replace(/^(https?:\/\/|rtsp:\/\/)/, '')
      cleanIp = cleanIp.replace(/\/$/, '') // Remove trailing slash

      // Ensure stream path starts with /
      const streamPath = formData.streamPath.startsWith('/')
        ? formData.streamPath
        : `/${formData.streamPath}`

      return `rtsp://${auth}${cleanIp}:${formData.port}${streamPath}`
    }
    return ''
  }

  const handleDetectionTypeToggle = (type: string) => {
    setFormData(prev => ({
      ...prev,
      detectionTypes: prev.detectionTypes.includes(type)
        ? prev.detectionTypes.filter(t => t !== type)
        : [...prev.detectionTypes, type]
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const rtspUrl = generateRtspUrl()

      const payload = {
        name: formData.name,
        description: formData.description,
        stream_url: rtspUrl,
        camera_type: formData.cameraType,
        location: formData.location,
        detection_types: formData.detectionTypes,
        confidence_threshold: formData.confidenceThreshold,
        alert_enabled: formData.alertEnabled,
      }

      const response = await fetch(`${API_URL}/api/camera/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      if (response.ok) {
        const newCamera = await response.json()

        // Add to cameras list
        setCameras(prev => [...prev, {
          id: newCamera.id,
          name: newCamera.name,
          location: newCamera.location,
          status: 'inactive',
          type: newCamera.camera_type.toUpperCase(),
          rtspUrl: newCamera.stream_url,
          detectionTypes: newCamera.detection_types,
          confidenceThreshold: newCamera.confidence_threshold,
          fps: 0,
          resolution: '1920x1080',
          uptime: '0h',
          lastUpdated: 'Just now'
        }])

        // Reset form and close modal
        setFormData({
          name: '',
          description: '',
          cameraType: 'rtsp',
          ipAddress: '',
          port: '554',
          username: '',
          password: '',
          streamPath: '/Streaming/Channels/101',
          location: '',
          detectionTypes: [],
          confidenceThreshold: 0.5,
          alertEnabled: true,
        })
        setShowAddModal(false)
        alert('✅ Camera added successfully!')
      } else {
        const error = await response.json()
        alert(`❌ Failed to add camera: ${error.detail || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('Error adding camera:', error)
      alert('❌ Failed to add camera. Please check your connection.')
    } finally {
      setLoading(false)
    }
  }

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
              <h1 className="text-4xl font-bold text-gray-900 mb-2">Camera Management</h1>
              <p className="text-gray-600">Configure and monitor your RTSP camera feeds</p>
            </div>
            <button
              onClick={() => setShowAddModal(true)}
              className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-shadow flex items-center space-x-2"
            >
              <FaPlus />
              <span>Add Camera</span>
            </button>
          </motion.div>

          {/* Empty State - Show when no cameras */}
          {cameras.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl shadow-xl p-12 text-center"
            >
              <div className="max-w-md mx-auto">
                <div className="mb-6 inline-block p-6 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full">
                  <FaCamera className="text-6xl text-blue-600" />
                </div>
                <h2 className="text-3xl font-bold text-gray-900 mb-4">No Cameras Added Yet</h2>
                <p className="text-gray-600 mb-8 text-lg leading-relaxed">
                  Get started by adding your first RTSP camera to begin monitoring with AI-powered detection.
                  Connect your IP cameras and start detecting PPE compliance, falls, fire, and smoke in real-time.
                </p>
                <button
                  onClick={() => setShowAddModal(true)}
                  className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-bold hover:shadow-xl transition-all transform hover:-translate-y-1 flex items-center space-x-3 mx-auto"
                >
                  <FaPlus className="text-xl" />
                  <span>Add Your First Camera</span>
                </button>

                <div className="mt-12 pt-8 border-t border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">📹 Supported Camera Types</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div className="p-4 bg-blue-50 rounded-lg">
                      <p className="font-semibold text-blue-900">RTSP Cameras</p>
                      <p className="text-blue-700 text-xs mt-1">IP cameras with RTSP protocol</p>
                    </div>
                    <div className="p-4 bg-purple-50 rounded-lg">
                      <p className="font-semibold text-purple-900">Network Cameras</p>
                      <p className="text-purple-700 text-xs mt-1">HTTP/HTTPS video streams</p>
                    </div>
                    <div className="p-4 bg-pink-50 rounded-lg">
                      <p className="font-semibold text-pink-900">USB Cameras</p>
                      <p className="text-pink-700 text-xs mt-1">Local USB webcams</p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          ) : (
            /* Camera Grid - Show when cameras exist */
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

              {cameras.map((camera, index) => (
                <motion.div
                  key={camera.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-gray-900 mb-1">{camera.name}</h3>
                      <p className="text-sm text-gray-600 mb-2">{camera.location}</p>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded font-semibold">
                          {camera.type || 'RTSP'}
                        </span>
                        {camera.rtspUrl && (
                          <span className="text-xs text-gray-500 truncate max-w-[200px]" title={camera.rtspUrl}>
                            {camera.rtspUrl}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex flex-col items-end space-y-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold flex items-center space-x-1 ${
                        camera.status === 'active'
                          ? 'bg-green-100 text-green-800'
                          : camera.status === 'error'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {camera.status === 'active' && <FaCheckCircle />}
                        {camera.status === 'error' && <FaTimesCircle />}
                        {camera.status === 'inactive' && <FaExclamationTriangle />}
                        <span className="capitalize">{camera.status}</span>
                      </span>
                    </div>
                  </div>

                  {/* Detection Alerts */}
                  {detectionAlerts[camera.id] && detectionAlerts[camera.id].length > 0 && (
                    <div className="mb-3 flex flex-wrap gap-2">
                      {detectionAlerts[camera.id].some((d: any) => d.type === 'fall') && (
                        <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-xs font-bold flex items-center space-x-1 animate-pulse">
                          <span>🚨</span>
                          <span>FALL DETECTED</span>
                        </span>
                      )}
                      {detectionAlerts[camera.id].some((d: any) => d.type === 'fire') && (
                        <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-xs font-bold flex items-center space-x-1 animate-pulse">
                          <span>🔥</span>
                          <span>FIRE DETECTED</span>
                        </span>
                      )}
                      {detectionAlerts[camera.id].some((d: any) => d.type === 'smoke') && (
                        <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-bold flex items-center space-x-1 animate-pulse">
                          <span>💨</span>
                          <span>SMOKE DETECTED</span>
                        </span>
                      )}
                      {detectionAlerts[camera.id].filter((d: any) => d.type === 'ppe').length > 0 && (
                        <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-bold flex items-center space-x-1">
                          <span>🦺</span>
                          <span>{detectionAlerts[camera.id].filter((d: any) => d.type === 'ppe').length} PPE Items</span>
                        </span>
                      )}
                    </div>
                  )}

                  {/* Video Feed Display */}
                  <div className="bg-gray-900 rounded-lg h-48 mb-4 flex items-center justify-center relative overflow-hidden group">
                    {streamFrames[camera.id] ? (
                      // Show live feed
                      <img
                        src={streamFrames[camera.id]}
                        alt={`Live feed from ${camera.name}`}
                        className="w-full h-full object-cover cursor-pointer"
                        onClick={() => setFullscreenCamera(camera.id)}
                      />
                    ) : (
                      // Show placeholder when no stream
                      <div className="flex flex-col items-center justify-center space-y-2">
                        <FaVideo className="text-6xl text-gray-600" />
                        {camera.status === 'inactive' && (
                          <p className="text-xs text-gray-500">Click Start to view live feed</p>
                        )}
                        {camera.status === 'error' && (
                          <p className="text-xs text-red-500">Connection failed</p>
                        )}
                      </div>
                    )}

                    {/* LIVE Indicator with FPS */}
                    {camera.status === 'active' && streamFrames[camera.id] && (
                      <div className="absolute top-2 right-2 flex items-center space-x-2">
                        <div className="flex items-center space-x-1 bg-red-600 text-white px-2 py-1 rounded text-xs font-semibold shadow-lg">
                          <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
                          <span>LIVE</span>
                        </div>
                        {streamFps[camera.id] && (
                          <div className="bg-black bg-opacity-70 text-white px-2 py-1 rounded text-xs font-semibold shadow-lg">
                            {streamFps[camera.id]} FPS
                          </div>
                        )}
                      </div>
                    )}

                    {/* Fullscreen Button (appears on hover) */}
                    {streamFrames[camera.id] && (
                      <button
                        onClick={() => setFullscreenCamera(camera.id)}
                        className="absolute top-2 left-2 bg-black bg-opacity-70 text-white p-2 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-opacity-90"
                        title="View Fullscreen"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                        </svg>
                      </button>
                    )}

                    {/* Camera Info Overlay */}
                    <div className="absolute bottom-2 left-2 bg-black bg-opacity-60 text-white px-2 py-1 rounded text-xs">
                      {camera.name}
                    </div>
                  </div>

                  {/* Camera Stats */}
                  <div className="grid grid-cols-3 gap-2 mb-4">
                    <div className="bg-blue-50 rounded-lg p-2 text-center">
                      <p className="text-xs text-gray-600">FPS</p>
                      <p className="text-lg font-bold text-blue-600">{streamFps[camera.id] || camera.fps || 0}</p>
                    </div>
                    <div className="bg-purple-50 rounded-lg p-2 text-center">
                      <p className="text-xs text-gray-600">Resolution</p>
                      <p className="text-sm font-bold text-purple-600">{camera.resolution || '1920x1080'}</p>
                    </div>
                    <div className="bg-pink-50 rounded-lg p-2 text-center">
                      <p className="text-xs text-gray-600">Uptime</p>
                      <p className="text-sm font-bold text-pink-600">{camera.uptime || '0h'}</p>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex justify-between items-center">
                    <div className="text-xs text-gray-500">
                      Last updated: {camera.lastUpdated || 'Just now'}
                    </div>
                    <div className="flex space-x-2">
                      {camera.status === 'active' ? (
                        <button
                          onClick={() => stopCameraStream(camera)}
                          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center space-x-2 text-sm"
                        >
                          <FaStop />
                          <span>Stop</span>
                        </button>
                      ) : (
                        <button
                          onClick={() => startCameraStream(camera)}
                          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2 text-sm"
                        >
                          <FaPlay />
                          <span>Start</span>
                        </button>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}

          {/* Info Banner - Only show when cameras exist */}
          {cameras.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-6"
            >
              <h3 className="text-lg font-bold text-blue-900 mb-2">💡 Pro Tip</h3>
              <p className="text-blue-800 mb-4">
                Monitor your RTSP camera feeds in real-time with AI-powered detection.
                Configure detection types, set confidence thresholds, and receive instant alerts.
              </p>
              <Link href="/detection">
                <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  Try Detection Demo
                </button>
              </Link>
            </motion.div>
          )}
        </div>
      </div>

      <Footer />

      {/* Add Camera Modal */}
      <AnimatePresence>
        {showAddModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
            onClick={() => setShowAddModal(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Modal Header */}
              <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-2xl flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold">Add New Camera</h2>
                  <p className="text-blue-100 text-sm mt-1">Configure your RTSP camera connection</p>
                </div>
                <button
                  onClick={() => setShowAddModal(false)}
                  className="p-2 hover:bg-white hover:bg-opacity-20 rounded-lg transition-colors"
                >
                  <FaTimes className="text-2xl" />
                </button>
              </div>

              {/* Modal Body */}
              <form onSubmit={handleSubmit} className="p-6 space-y-6">
                {/* Camera Basic Info */}
                <div className="space-y-4">
                  <h3 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
                    <FaCamera className="text-blue-600" />
                    <span>Camera Information</span>
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        Camera Name <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        required
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        placeholder="e.g., Warehouse A - Main Entrance"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        Location
                      </label>
                      <input
                        type="text"
                        value={formData.location}
                        onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                        placeholder="e.g., Building A - Floor 1"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Description
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      placeholder="Optional description of the camera"
                      rows={2}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                {/* RTSP Connection Settings */}
                <div className="space-y-4 pt-4 border-t border-gray-200">
                  <h3 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
                    <FaVideo className="text-purple-600" />
                    <span>RTSP Connection Settings</span>
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        Camera IP Address <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        required
                        value={formData.ipAddress}
                        onChange={(e) => setFormData({ ...formData, ipAddress: e.target.value })}
                        placeholder="e.g., 192.168.1.172"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        Enter IP address only (e.g., 192.168.1.172) - no http:// or rtsp://
                      </p>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        RTSP Port
                      </label>
                      <input
                        type="text"
                        value={formData.port}
                        onChange={(e) => setFormData({ ...formData, port: e.target.value })}
                        placeholder="554"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      <p className="text-xs text-gray-500 mt-1">Default: 554</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        Username <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        required
                        value={formData.username}
                        onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                        placeholder="e.g., admin"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        Password <span className="text-red-500">*</span>
                      </label>
                      <div className="relative">
                        <input
                          type={showPassword ? 'text' : 'password'}
                          required
                          value={formData.password}
                          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                          placeholder="Enter camera password"
                          className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                        >
                          {showPassword ? <FaEyeSlash /> : <FaEye />}
                        </button>
                      </div>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Stream Path
                    </label>
                    <input
                      type="text"
                      value={formData.streamPath}
                      onChange={(e) => setFormData({ ...formData, streamPath: e.target.value })}
                      placeholder="/cam/realmonitor?channel=1&subtype=1"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      <strong>Dahua:</strong> /cam/realmonitor?channel=1&subtype=1 (sub stream) or subtype=0 (main stream)<br />
                      <strong>Hikvision:</strong> /Streaming/Channels/101 (main) or /Streaming/Channels/102 (sub)
                    </p>
                  </div>

                  {/* Generated RTSP URL Preview */}
                  {generateRtspUrl() && (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <p className="text-sm font-semibold text-blue-900 mb-1">Generated RTSP URL:</p>
                      <code className="text-xs text-blue-700 break-all">
                        {generateRtspUrl().replace(formData.password, '****')}
                      </code>
                    </div>
                  )}
                </div>

                {/* Detection Settings */}
                <div className="space-y-4 pt-4 border-t border-gray-200">
                  <h3 className="text-lg font-bold text-gray-900">AI Detection Settings</h3>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Detection Types <span className="text-red-500">*</span>
                    </label>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {[
                        { id: 'ppe', label: 'PPE Detection', color: 'blue' },
                        { id: 'fall', label: 'Fall Detection', color: 'red' },
                        { id: 'fire', label: 'Fire Detection', color: 'orange' },
                        { id: 'smoke', label: 'Smoke Detection', color: 'gray' },
                      ].map((type) => (
                        <button
                          key={type.id}
                          type="button"
                          onClick={() => handleDetectionTypeToggle(type.id)}
                          className={`p-3 rounded-lg border-2 transition-all ${
                            formData.detectionTypes.includes(type.id)
                              ? `border-${type.color}-500 bg-${type.color}-50 text-${type.color}-700`
                              : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
                          }`}
                        >
                          <div className="flex items-center justify-center space-x-2">
                            <input
                              type="checkbox"
                              checked={formData.detectionTypes.includes(type.id)}
                              onChange={() => {}}
                              className="w-4 h-4"
                            />
                            <span className="text-sm font-semibold">{type.label}</span>
                          </div>
                        </button>
                      ))}
                    </div>
                    {formData.detectionTypes.length === 0 && (
                      <p className="text-xs text-red-500 mt-2">Please select at least one detection type</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Confidence Threshold: {formData.confidenceThreshold.toFixed(2)}
                    </label>
                    <input
                      type="range"
                      min="0.1"
                      max="0.9"
                      step="0.05"
                      value={formData.confidenceThreshold}
                      onChange={(e) => setFormData({ ...formData, confidenceThreshold: parseFloat(e.target.value) })}
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>Low (0.1) - More detections</span>
                      <span>High (0.9) - Fewer, more accurate</span>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      id="alertEnabled"
                      checked={formData.alertEnabled}
                      onChange={(e) => setFormData({ ...formData, alertEnabled: e.target.checked })}
                      className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <label htmlFor="alertEnabled" className="text-sm font-semibold text-gray-700">
                      Enable alerts for detections
                    </label>
                  </div>
                </div>

                {/* Form Actions */}
                <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-semibold"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading || formData.detectionTypes.length === 0}
                    className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                  >
                    {loading ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        <span>Adding Camera...</span>
                      </>
                    ) : (
                      <>
                        <FaPlus />
                        <span>Add Camera</span>
                      </>
                    )}
                  </button>
                </div>

                {/* Help Text */}
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <h4 className="text-sm font-bold text-yellow-900 mb-2">📌 Quick Tips:</h4>
                  <ul className="text-xs text-yellow-800 space-y-1 list-disc list-inside">
                    <li>Make sure your camera is on the same network or accessible via VPN</li>
                    <li>Test the camera connection using VLC or another RTSP player first</li>
                    <li>Common RTSP ports: 554 (default), 8554, 88</li>
                    <li>For Hikvision cameras, use: /Streaming/Channels/101 (main stream) or /Streaming/Channels/102 (sub stream)</li>
                    <li>For Dahua cameras, use: /cam/realmonitor?channel=1&subtype=0</li>
                  </ul>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Fullscreen Camera Modal */}
      <AnimatePresence>
        {fullscreenCamera !== null && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-95 z-50 flex items-center justify-center p-4"
            onClick={() => setFullscreenCamera(null)}
          >
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              className="relative w-full h-full max-w-7xl max-h-screen"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Close Button */}
              <button
                onClick={() => setFullscreenCamera(null)}
                className="absolute top-4 right-4 z-10 bg-red-600 hover:bg-red-700 text-white p-3 rounded-full shadow-lg transition-colors"
              >
                <FaTimes className="text-xl" />
              </button>

              {/* Camera Info Header */}
              {cameras.find(c => c.id === fullscreenCamera) && (
                <div className="absolute top-4 left-4 z-10 bg-black bg-opacity-70 text-white px-4 py-2 rounded-lg">
                  <h3 className="text-lg font-bold">{cameras.find(c => c.id === fullscreenCamera)?.name}</h3>
                  <p className="text-sm text-gray-300">{cameras.find(c => c.id === fullscreenCamera)?.location}</p>
                  {streamFps[fullscreenCamera] && (
                    <p className="text-xs text-green-400 mt-1">
                      {streamFps[fullscreenCamera]} FPS
                    </p>
                  )}
                </div>
              )}

              {/* Detection Alerts in Fullscreen */}
              {detectionAlerts[fullscreenCamera] && detectionAlerts[fullscreenCamera].length > 0 && (
                <div className="absolute bottom-4 left-4 z-10 flex flex-wrap gap-2">
                  {detectionAlerts[fullscreenCamera].some((d: any) => d.type === 'fall') && (
                    <span className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-bold flex items-center space-x-2 animate-pulse shadow-lg">
                      <span className="text-2xl">🚨</span>
                      <span>FALL DETECTED</span>
                    </span>
                  )}
                  {detectionAlerts[fullscreenCamera].some((d: any) => d.type === 'fire') && (
                    <span className="px-4 py-2 bg-orange-600 text-white rounded-lg text-sm font-bold flex items-center space-x-2 animate-pulse shadow-lg">
                      <span className="text-2xl">🔥</span>
                      <span>FIRE DETECTED</span>
                    </span>
                  )}
                  {detectionAlerts[fullscreenCamera].some((d: any) => d.type === 'smoke') && (
                    <span className="px-4 py-2 bg-gray-700 text-white rounded-lg text-sm font-bold flex items-center space-x-2 animate-pulse shadow-lg">
                      <span className="text-2xl">💨</span>
                      <span>SMOKE DETECTED</span>
                    </span>
                  )}
                  {detectionAlerts[fullscreenCamera].filter((d: any) => d.type === 'ppe').length > 0 && (
                    <span className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-bold flex items-center space-x-2 shadow-lg">
                      <span className="text-2xl">🦺</span>
                      <span>{detectionAlerts[fullscreenCamera].filter((d: any) => d.type === 'ppe').length} PPE Items Detected</span>
                    </span>
                  )}
                </div>
              )}

              {/* Fullscreen Video */}
              <div className="w-full h-full flex items-center justify-center bg-black rounded-lg overflow-hidden">
                {streamFrames[fullscreenCamera] ? (
                  <img
                    src={streamFrames[fullscreenCamera]}
                    alt="Fullscreen camera view"
                    className="max-w-full max-h-full object-contain"
                  />
                ) : (
                  <div className="text-white text-center">
                    <FaVideo className="text-6xl mb-4 mx-auto opacity-50" />
                    <p>No stream available</p>
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  )
}

