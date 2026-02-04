'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { FaUpload, FaSpinner, FaCheckCircle, FaExclamationCircle } from 'react-icons/fa'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function DetectionPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [error, setError] = useState<string>('')
  const [detectionTypes, setDetectionTypes] = useState({
    ppe: false,
    fall: false,
    fire: false,
    smoke: false,
    roi: false,
    lineCrossing: false,
    crowdDensity: false,
    loitering: false,
    intrusion: false
  })
  // Removed ppeTypes state - now detecting ALL 17 classes automatically
  const [confidence, setConfidence] = useState(0.5)

  // Handle detection type selection with mutual exclusivity
  // PPE and Fall are mutually exclusive with Fire/Smoke group
  // Fire and Smoke can be selected together
  const handleDetectionTypeChange = (type: string, checked: boolean) => {
    if (type === 'ppe' && checked) {
      // If PPE is selected, uncheck Fall, Fire, and Smoke
      setDetectionTypes({
        ...detectionTypes,
        ppe: true,
        fall: false,
        fire: false,
        smoke: false
      })
    } else if (type === 'fall' && checked) {
      // If Fall is selected, uncheck PPE, Fire, and Smoke
      setDetectionTypes({
        ...detectionTypes,
        ppe: false,
        fall: true,
        fire: false,
        smoke: false
      })
    } else if ((type === 'fire' || type === 'smoke') && checked) {
      // If Fire or Smoke is selected, uncheck PPE and Fall
      // But keep Fire and Smoke together
      setDetectionTypes({
        ...detectionTypes,
        ppe: false,
        fall: false,
        [type]: true
      })
    } else {
      // Just toggle the checkbox normally (for unchecking)
      setDetectionTypes({
        ...detectionTypes,
        [type]: checked
      })
    }
  }

  // Download handler for annotated files
  const handleDownload = async (url: string, filename: string) => {
    try {
      const response = await fetch(`${API_URL}${url}`)
      const blob = await response.blob()
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
    } catch (error) {
      console.error('Download failed:', error)
      alert('Failed to download file. Please try again.')
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setResults(null)
      setError('')
    }
  }

  const handleDetect = async () => {
    if (!selectedFile) {
      setError('Please select a file first')
      return
    }

    setLoading(true)
    setError('')
    setResults(null)

    try {
      // Determine which detection to run based on selected types
      const enabledTypes = Object.entries(detectionTypes)
        .filter(([_, enabled]) => enabled)
        .map(([type, _]) => type)

      if (enabledTypes.length === 0) {
        setError('Please select at least one detection type')
        setLoading(false)
        return
      }

      // For now, prioritize fire/smoke detection if both fire and smoke are selected
      if (enabledTypes.includes('fire') || enabledTypes.includes('smoke')) {
        await handleFireSmokeDetection(enabledTypes)
      } else if (enabledTypes.includes('ppe')) {
        await handlePPEDetection()
      } else if (enabledTypes.includes('fall')) {
        await handleFallDetection()
      } else {
        setError('Please select a valid detection type')
      }
    } catch (err: any) {
      console.error('Detection error:', err)
      console.error('Error response:', err.response)
      console.error('Error message:', err.message)
      console.error('Error stack:', err.stack)
      setError(err.response?.data?.detail || err.message || 'Detection failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleFireSmokeDetection = async (enabledTypes: string[]) => {
    const formData = new FormData()
    formData.append('file', selectedFile!)

    // Determine detection mode
    let detectionMode = 'both'
    if (enabledTypes.includes('fire') && !enabledTypes.includes('smoke')) {
      detectionMode = 'fire'
    } else if (enabledTypes.includes('smoke') && !enabledTypes.includes('fire')) {
      detectionMode = 'smoke'
    }

    formData.append('detection_mode', detectionMode)
    formData.append('confidence', confidence.toString())
    formData.append('draw_boxes', 'true')

    const response = await axios.post(`${API_URL}/api/detection/fire-smoke`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    setResults(response.data)

    // Update preview with annotated image/video if available
    if (response.data.annotated_video_url) {
      setPreviewUrl(`${API_URL}${response.data.annotated_video_url}`)
    } else if (response.data.annotated_image_url) {
      setPreviewUrl(`${API_URL}${response.data.annotated_image_url}`)
    }
  }

  const handlePPEDetection = async () => {
    const formData = new FormData()
    formData.append('file', selectedFile!)

    // No ppe_types filter - detect ALL 17 classes automatically
    // Removed filtering logic for better performance

    formData.append('confidence', confidence.toString())
    formData.append('draw_boxes', 'true')

    const response = await axios.post(`${API_URL}/api/detection/ppe`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    setResults(response.data)

    // Update preview with annotated image/video if available
    if (response.data.annotated_video_url) {
      setPreviewUrl(`${API_URL}${response.data.annotated_video_url}`)
    } else if (response.data.annotated_image_url) {
      setPreviewUrl(`${API_URL}${response.data.annotated_image_url}`)
    }
  }

  const handleFallDetection = async () => {
    const formData = new FormData()
    formData.append('file', selectedFile!)
    formData.append('confidence', confidence.toString())
    formData.append('draw_boxes', 'true')

    console.log('Sending fall detection request to:', `${API_URL}/api/detection/fall`)

    const response = await axios.post(`${API_URL}/api/detection/fall`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    console.log('Fall detection response:', response.data)
    console.log('Response status:', response.status)
    console.log('Annotated video URL:', response.data.annotated_video_url)
    console.log('Annotated image URL:', response.data.annotated_image_url)

    setResults(response.data)

    // Update preview with annotated image/video if available
    if (response.data.annotated_video_url) {
      console.log('Setting preview URL to video:', `${API_URL}${response.data.annotated_video_url}`)
      setPreviewUrl(`${API_URL}${response.data.annotated_video_url}`)
    } else if (response.data.annotated_image_url) {
      console.log('Setting preview URL to image:', `${API_URL}${response.data.annotated_image_url}`)
      setPreviewUrl(`${API_URL}${response.data.annotated_image_url}`)
    } else {
      console.log('No annotated video or image URL in response')
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100">
      <Navbar />

      <div className="pt-32 pb-20 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-6">
              Intelligent Video <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">Analytics</span>
            </h1>
            <p className="text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Experience enterprise-grade computer vision with real-time object detection, behavioral analysis,
              perimeter security, and compliance monitoring—all powered by advanced AI
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-3 text-sm">
              <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full font-semibold">Safety Compliance</span>
              <span className="px-4 py-2 bg-purple-100 text-purple-700 rounded-full font-semibold">Incident Detection</span>
              <span className="px-4 py-2 bg-pink-100 text-pink-700 rounded-full font-semibold">Perimeter Security</span>
              <span className="px-4 py-2 bg-green-100 text-green-700 rounded-full font-semibold">ROI Monitoring</span>
              <span className="px-4 py-2 bg-orange-100 text-orange-700 rounded-full font-semibold">Line Crossing</span>
            </div>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-10">
            {/* Upload Section */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100"
            >
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Upload Image</h2>
              
              {/* File Upload */}
              <div className="mb-6">
                <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-500 transition-colors">
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <FaUpload className="text-4xl text-gray-400 mb-3" />
                    <p className="mb-2 text-sm text-gray-500">
                      <span className="font-semibold">Click to upload</span> or drag and drop
                    </p>
                    <p className="text-xs text-gray-500">Images: PNG, JPG, JPEG | Videos: MP4, AVI, MOV (MAX. 100MB)</p>
                  </div>
                  <input
                    type="file"
                    className="hidden"
                    accept="image/*,video/*"
                    onChange={handleFileSelect}
                  />
                </label>
              </div>

              {/* Detection Types */}
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-2 text-lg">AI Detection Capabilities</h3>
                <p className="text-xs text-gray-600 mb-4 bg-blue-50 p-2 rounded border border-blue-200">
                  💡 <strong>Selection Rules:</strong> Choose PPE <strong>OR</strong> Fall <strong>OR</strong> Fire/Smoke. Fire and Smoke can be selected together.
                </p>

                {/* Safety & Compliance */}
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-blue-600 mb-2 uppercase tracking-wide">Safety & Compliance</h4>
                  <div className="space-y-2 pl-2">
                    <label className="flex items-center space-x-2 cursor-pointer group">
                      <input
                        type="checkbox"
                        checked={detectionTypes.ppe}
                        onChange={(e) => handleDetectionTypeChange('ppe', e.target.checked)}
                        className="w-4 h-4 text-blue-600 rounded"
                      />
                      <span className="text-gray-700 group-hover:text-blue-600 transition-colors">🦺 PPE Compliance Detection</span>
                    </label>
                    <label className="flex items-center space-x-2 cursor-pointer group">
                      <input
                        type="checkbox"
                        checked={detectionTypes.fall}
                        onChange={(e) => handleDetectionTypeChange('fall', e.target.checked)}
                        className="w-4 h-4 text-blue-600 rounded"
                      />
                      <span className="text-gray-700 group-hover:text-blue-600 transition-colors">🤸 Fall & Incident Detection</span>
                    </label>
                  </div>
                </div>

                {/* Hazard Detection */}
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-orange-600 mb-2 uppercase tracking-wide">Hazard Detection</h4>
                  <div className="space-y-2 pl-2">
                    <label className="flex items-center space-x-2 cursor-pointer group">
                      <input
                        type="checkbox"
                        checked={detectionTypes.fire}
                        onChange={(e) => handleDetectionTypeChange('fire', e.target.checked)}
                        className="w-4 h-4 text-orange-600 rounded"
                      />
                      <span className="text-gray-700 group-hover:text-orange-600 transition-colors">🔥 Fire Detection</span>
                    </label>
                    <label className="flex items-center space-x-2 cursor-pointer group">
                      <input
                        type="checkbox"
                        checked={detectionTypes.smoke}
                        onChange={(e) => handleDetectionTypeChange('smoke', e.target.checked)}
                        className="w-4 h-4 text-orange-600 rounded"
                      />
                      <span className="text-gray-700 group-hover:text-orange-600 transition-colors">💨 Smoke Detection</span>
                    </label>
                  </div>
                </div>

                {/* Perimeter & Access Control */}
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-purple-600 mb-2 uppercase tracking-wide flex items-center">
                    Perimeter & Access Control
                    <span className="ml-2 text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">Coming Soon</span>
                  </h4>
                  <div className="space-y-2 pl-2 opacity-60">
                    <label className="flex items-center space-x-2 cursor-not-allowed group">
                      <input
                        type="checkbox"
                        checked={detectionTypes.roi}
                        onChange={(e) => setDetectionTypes({...detectionTypes, roi: e.target.checked})}
                        className="w-4 h-4 text-purple-600 rounded"
                        disabled
                      />
                      <span className="text-gray-700">📍 ROI (Region of Interest) Monitoring</span>
                    </label>
                    <label className="flex items-center space-x-2 cursor-not-allowed group">
                      <input
                        type="checkbox"
                        checked={detectionTypes.lineCrossing}
                        onChange={(e) => setDetectionTypes({...detectionTypes, lineCrossing: e.target.checked})}
                        className="w-4 h-4 text-purple-600 rounded"
                        disabled
                      />
                      <span className="text-gray-700">↔️ Line Crossing Detection</span>
                    </label>
                    <label className="flex items-center space-x-2 cursor-not-allowed group">
                      <input
                        type="checkbox"
                        checked={detectionTypes.intrusion}
                        onChange={(e) => setDetectionTypes({...detectionTypes, intrusion: e.target.checked})}
                        className="w-4 h-4 text-purple-600 rounded"
                        disabled
                      />
                      <span className="text-gray-700">🚨 Intrusion Detection</span>
                    </label>
                  </div>
                </div>

                {/* Behavioral Analytics */}
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-green-600 mb-2 uppercase tracking-wide flex items-center">
                    Behavioral Analytics
                    <span className="ml-2 text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">Coming Soon</span>
                  </h4>
                  <div className="space-y-2 pl-2 opacity-60">
                    <label className="flex items-center space-x-2 cursor-not-allowed group">
                      <input
                        type="checkbox"
                        checked={detectionTypes.crowdDensity}
                        onChange={(e) => setDetectionTypes({...detectionTypes, crowdDensity: e.target.checked})}
                        className="w-4 h-4 text-green-600 rounded"
                        disabled
                      />
                      <span className="text-gray-700">👥 Crowd Density Analysis</span>
                    </label>
                    <label className="flex items-center space-x-2 cursor-not-allowed group">
                      <input
                        type="checkbox"
                        checked={detectionTypes.loitering}
                        onChange={(e) => setDetectionTypes({...detectionTypes, loitering: e.target.checked})}
                        className="w-4 h-4 text-green-600 rounded"
                        disabled
                      />
                      <span className="text-gray-700">⏱️ Loitering Detection</span>
                    </label>
                  </div>
                </div>
              </div>

              {/* PPE Detection Info (shown when PPE is selected) */}
              {detectionTypes.ppe && (
                <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <h3 className="font-semibold text-gray-900 mb-3">✅ PPE Detection Enabled</h3>
                  <p className="text-sm text-gray-700">
                    Automatically detecting <strong>all 17 PPE classes</strong>:
                  </p>
                  <div className="mt-2 text-xs text-gray-600 grid grid-cols-2 gap-1">
                    <span>• Person</span>
                    <span>• Helmet</span>
                    <span>• Safety Vest</span>
                    <span>• Gloves</span>
                    <span>• Glasses</span>
                    <span>• Face Mask</span>
                    <span>• Shoes</span>
                    <span>• Safety Suit</span>
                    <span>• Medical Suit</span>
                    <span>• Ear Protection</span>
                    <span>• Ear Muffs</span>
                    <span>• Face Guard</span>
                    <span>• Face</span>
                    <span>• Hands</span>
                    <span>• Head</span>
                    <span>• Foot</span>
                    <span>• Tool</span>
                  </div>
                  <p className="text-xs text-gray-500 mt-3">
                    No filtering applied - maximum performance and accuracy
                  </p>
                </div>
              )}

              {/* Confidence Threshold */}
              <div className="mb-6">
                <label className="block font-semibold text-gray-900 mb-2">
                  Confidence Threshold: {confidence.toFixed(2)}
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={confidence}
                  onChange={(e) => setConfidence(parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>

              {/* Detect Button */}
              <button
                onClick={handleDetect}
                disabled={!selectedFile || loading || (!detectionTypes.ppe && !detectionTypes.fall && !detectionTypes.fire && !detectionTypes.smoke)}
                className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <FaSpinner className="animate-spin" />
                    <span>Detecting...</span>
                  </>
                ) : (
                  <span>Run Detection</span>
                )}
              </button>

              {/* Validation Message */}
              {!detectionTypes.ppe && !detectionTypes.fall && !detectionTypes.fire && !detectionTypes.smoke && (
                <div className="text-sm text-orange-600 bg-orange-50 p-3 rounded-lg border border-orange-200">
                  ⚠️ Please select at least one detection type above
                </div>
              )}

              {/* Error Message */}
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-2">
                  <FaExclamationCircle className="text-red-600 mt-0.5" />
                  <p className="text-red-800 text-sm">{error}</p>
                </div>
              )}
            </motion.div>

            {/* Results Section */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-xl shadow-lg p-6"
            >
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Results</h2>
              
              {/* Image/Video Preview */}
              {previewUrl && (
                <div className="mb-4">
                  {selectedFile?.type.startsWith('video/') ? (
                    <video
                      src={previewUrl}
                      controls
                      className="w-full rounded-lg"
                    />
                  ) : (
                    <img
                      src={previewUrl}
                      alt="Preview"
                      className="w-full rounded-lg"
                    />
                  )}
                </div>
              )}

              {/* Detection Results */}
              {results && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-2 text-green-600">
                    <FaCheckCircle />
                    <span className="font-semibold">Detection Complete!</span>
                  </div>

                  {/* Video Info (if video) */}
                  {results.file_type === 'video' && results.video_info && (
                    <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                      <h3 className="font-semibold text-purple-900 mb-2">Video Information</h3>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div>
                          <span className="text-gray-600">Duration:</span>
                          <span className="ml-2 font-semibold">{results.video_info.duration_seconds?.toFixed(1)}s</span>
                        </div>
                        <div>
                          <span className="text-gray-600">FPS:</span>
                          <span className="ml-2 font-semibold">{results.video_info.fps}</span>
                        </div>
                        <div>
                          <span className="text-gray-600">Total Frames:</span>
                          <span className="ml-2 font-semibold">{results.video_info.total_frames}</span>
                        </div>
                        <div>
                          <span className="text-gray-600">Resolution:</span>
                          <span className="ml-2 font-semibold">{results.video_info.resolution}</span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* PPE Detection Results */}
                  {results.compliance_status && (
                    <div className={`p-4 rounded-lg border ${
                      results.compliance_status === 'compliant' ? 'bg-green-50 border-green-200' :
                      results.compliance_status === 'partial' ? 'bg-yellow-50 border-yellow-200' :
                      results.compliance_status === 'non-compliant' ? 'bg-red-50 border-red-200' :
                      'bg-gray-50 border-gray-200'
                    }`}>
                      <h3 className="font-semibold text-gray-900 mb-2">PPE Compliance Status</h3>
                      <div className="text-2xl font-bold capitalize mb-2">
                        {results.compliance_status === 'compliant' && '✅ Compliant'}
                        {results.compliance_status === 'partial' && '⚠️ Partial Compliance'}
                        {results.compliance_status === 'non-compliant' && '❌ Non-Compliant'}
                        {results.compliance_status === 'no-person' && '👤 No Person Detected'}
                      </div>
                      {results.persons_detected !== undefined && (
                        <p className="text-sm text-gray-600">
                          Persons detected: {results.persons_detected}
                        </p>
                      )}
                    </div>
                  )}

                  {/* PPE Items Detected */}
                  {results.ppe_counts && Object.keys(results.ppe_counts).length > 0 && (
                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <h3 className="font-semibold text-gray-900 mb-3">PPE Items Detected</h3>
                      <div className="grid grid-cols-2 gap-2">
                        {Object.entries(results.ppe_counts).map(([item, count]: [string, any]) => (
                          <div key={item} className="flex justify-between items-center p-2 bg-white rounded">
                            <span className="text-sm capitalize">{item.replace('-', ' ')}</span>
                            <span className="font-bold text-blue-600">{count}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* PPE Summary (for images) */}
                  {results.summary && results.summary.categories && (
                    <div className="p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                      <h3 className="font-semibold text-gray-900 mb-3">PPE Categories</h3>
                      <div className="space-y-2">
                        {Object.entries(results.summary.categories).map(([category, count]: [string, any]) => (
                          count > 0 && (
                            <div key={category} className="flex justify-between items-center">
                              <span className="text-sm capitalize">{category.replace('_', ' ')}</span>
                              <span className="font-semibold">{count}</span>
                            </div>
                          )
                        ))}
                      </div>
                    </div>
                  )}

                  {/* PPE Video Summary */}
                  {results.file_type === 'video' && results.summary && results.summary.overall_compliance && (
                    <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                      <h3 className="font-semibold text-gray-900 mb-3">Video Compliance Summary</h3>
                      <div className="grid grid-cols-3 gap-2 text-sm">
                        <div className="text-center p-2 bg-green-100 rounded">
                          <div className="font-bold text-green-700">{results.summary.compliant_frames}</div>
                          <div className="text-xs text-gray-600">Compliant</div>
                        </div>
                        <div className="text-center p-2 bg-yellow-100 rounded">
                          <div className="font-bold text-yellow-700">{results.summary.partial_frames}</div>
                          <div className="text-xs text-gray-600">Partial</div>
                        </div>
                        <div className="text-center p-2 bg-red-100 rounded">
                          <div className="font-bold text-red-700">{results.summary.non_compliant_frames}</div>
                          <div className="text-xs text-gray-600">Non-Compliant</div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Summary Stats */}
                  <div className="grid grid-cols-2 gap-4">
                    {results.file_type === 'video' && results.summary ? (
                      <>
                        <div className="p-4 bg-red-50 rounded-lg">
                          <p className="text-sm text-gray-600">Frames with Fire</p>
                          <p className="text-2xl font-bold text-red-600">
                            {results.summary.frames_with_fire}
                          </p>
                        </div>
                        <div className="p-4 bg-gray-50 rounded-lg">
                          <p className="text-sm text-gray-600">Frames with Smoke</p>
                          <p className="text-2xl font-bold text-gray-600">
                            {results.summary.frames_with_smoke}
                          </p>
                        </div>
                        <div className="p-4 bg-blue-50 rounded-lg">
                          <p className="text-sm text-gray-600">Detection Events</p>
                          <p className="text-2xl font-bold text-blue-600">
                            {results.summary.total_detection_events}
                          </p>
                        </div>
                        <div className={`p-4 rounded-lg ${
                          results.summary.alert_level === 'critical' ? 'bg-red-100' :
                          results.summary.alert_level === 'high' ? 'bg-orange-100' :
                          results.summary.alert_level === 'medium' ? 'bg-yellow-100' :
                          'bg-green-100'
                        }`}>
                          <p className="text-sm text-gray-600">Alert Level</p>
                          <p className="text-2xl font-bold capitalize">
                            {results.summary.alert_level}
                          </p>
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="p-4 bg-red-50 rounded-lg">
                          <p className="text-sm text-gray-600">Fire Detections</p>
                          <p className="text-2xl font-bold text-red-600">
                            {results.fire_detections?.length || 0}
                          </p>
                        </div>
                        <div className="p-4 bg-gray-50 rounded-lg">
                          <p className="text-sm text-gray-600">Smoke Detections</p>
                          <p className="text-2xl font-bold text-gray-600">
                            {results.smoke_detections?.length || 0}
                          </p>
                        </div>
                        <div className="p-4 bg-blue-50 rounded-lg">
                          <p className="text-sm text-gray-600">Total Detections</p>
                          <p className="text-2xl font-bold text-blue-600">
                            {results.total_detections}
                          </p>
                        </div>
                        <div className={`p-4 rounded-lg ${
                          results.alert_level === 'critical' ? 'bg-red-100' :
                          results.alert_level === 'high' ? 'bg-orange-100' :
                          results.alert_level === 'medium' ? 'bg-yellow-100' :
                          'bg-green-100'
                        }`}>
                          <p className="text-sm text-gray-600">Alert Level</p>
                          <p className="text-2xl font-bold capitalize">
                            {results.alert_level}
                          </p>
                        </div>
                      </>
                    )}
                  </div>

                  {/* Detection Details for Images */}
                  {results.file_type === 'image' && (results.fire_detections?.length > 0 || results.smoke_detections?.length > 0) && (
                    <div className="mt-4">
                      <h3 className="font-semibold text-gray-900 mb-2">Detections:</h3>
                      <div className="space-y-2 max-h-64 overflow-y-auto">
                        {[...(results.fire_detections || []), ...(results.smoke_detections || [])].map((det: any, idx: number) => (
                          <div key={idx} className="p-3 bg-gray-50 rounded-lg text-sm">
                            <p className="font-semibold capitalize">{det.class_name}</p>
                            <p className="text-gray-600">
                              Confidence: {(det.confidence * 100).toFixed(1)}%
                            </p>
                            <p className="text-gray-600 text-xs">
                              Type: {det.detection_type}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Frame Detections for Videos */}
                  {results.file_type === 'video' && results.frame_detections && results.frame_detections.length > 0 && (
                    <div className="mt-4">
                      <h3 className="font-semibold text-gray-900 mb-2">Detection Timeline (First 100 events):</h3>
                      <div className="space-y-2 max-h-64 overflow-y-auto">
                        {results.frame_detections.map((frame: any, idx: number) => (
                          <div key={idx} className="p-3 bg-gray-50 rounded-lg text-sm">
                            <div className="flex justify-between">
                              <span className="font-semibold">Frame {frame.frame}</span>
                              <span className="text-gray-600">{frame.timestamp?.toFixed(2)}s</span>
                            </div>
                            <div className="flex space-x-4 mt-1 text-xs">
                              {frame.fire_count > 0 && (
                                <span className="text-red-600">🔥 Fire: {frame.fire_count}</span>
                              )}
                              {frame.smoke_count > 0 && (
                                <span className="text-gray-600">💨 Smoke: {frame.smoke_count}</span>
                              )}
                              <span className={`capitalize ${
                                frame.alert_level === 'critical' ? 'text-red-600' :
                                frame.alert_level === 'high' ? 'text-orange-600' :
                                frame.alert_level === 'medium' ? 'text-yellow-600' :
                                'text-green-600'
                              }`}>
                                {frame.alert_level}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Annotated Image Download Link */}
                  {results.annotated_image_url && (
                    <div className="mt-4">
                      <button
                        onClick={() => handleDownload(
                          results.annotated_image_url,
                          `annotated_image_${Date.now()}.jpg`
                        )}
                        className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                      >
                        <FaCheckCircle className="mr-2" />
                        Download Annotated Image
                      </button>
                    </div>
                  )}

                  {/* Annotated Video Download Link */}
                  {results.annotated_video_url && (
                    <div className="mt-4">
                      <button
                        onClick={() => handleDownload(
                          results.annotated_video_url,
                          `annotated_video_${Date.now()}.mp4`
                        )}
                        className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        <FaCheckCircle className="mr-2" />
                        Download Annotated Video
                      </button>
                    </div>
                  )}
                </div>
              )}

              {!previewUrl && !results && (
                <div className="flex items-center justify-center h-64 text-gray-400">
                  <p>Upload an image or video to see results</p>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </div>

      <Footer />
    </main>
  )
}

