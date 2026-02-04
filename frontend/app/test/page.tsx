export default function TestPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
      <div className="text-center p-8">
        <h1 className="text-6xl font-bold mb-4">
          <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Gradient Test
          </span>
        </h1>
        <p className="text-2xl text-gray-700 mb-8">
          If you see this with a blue/white/purple gradient background, the styling is working!
        </p>
        <div className="space-y-4">
          <div className="p-4 bg-blue-100 rounded-lg">
            <p className="text-blue-900">✅ Blue section</p>
          </div>
          <div className="p-4 bg-purple-100 rounded-lg">
            <p className="text-purple-900">✅ Purple section</p>
          </div>
          <div className="p-4 bg-white rounded-lg shadow-lg">
            <p className="text-gray-900">✅ White section with shadow</p>
          </div>
        </div>
        <div className="mt-8">
          <a href="/" className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold inline-block hover:shadow-lg">
            Go to Home Page
          </a>
        </div>
      </div>
    </div>
  )
}

