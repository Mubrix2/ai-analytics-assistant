// frontend/src/App.jsx
import { useState, useEffect } from 'react'
import { askQuestion, getSampleQuestions, checkHealth } from './api/client'
import QueryInput from './components/QueryInput'
import SampleQuestions from './components/SampleQuestions'
import ChartDisplay from './components/ChartDisplay'
import SqlDisplay from './components/SqlDisplay'

export default function App() {
  // All state lives here — child components receive it as props
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [samples, setSamples] = useState([])
  const [isHealthy, setIsHealthy] = useState(true)

  // Runs once when the app loads
  useEffect(() => {
    async function init() {
      const healthy = await checkHealth()
      setIsHealthy(healthy)
      if (healthy) {
        const questions = await getSampleQuestions()
        setSamples(questions)
      }
    }
    init()
  }, [])

  async function handleQuestion(question) {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await askQuestion(question)
      setResult(data)
    } catch (err) {
      const message = err.response?.data?.detail || 'Something went wrong. Please try again.'
      setError(message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">
              AI Analytics Assistant
            </h1>
            <p className="text-xs text-gray-500">
              Ask questions about your sales data in plain English
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-green-400' : 'bg-red-400'}`} />
            <span className="text-xs text-gray-500">
              {isHealthy ? 'API connected' : 'API unreachable'}
            </span>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="max-w-4xl mx-auto px-6 py-8 space-y-6">

        {/* Query input */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
          <QueryInput onSubmit={handleQuestion} isLoading={isLoading} />
          <SampleQuestions questions={samples} onSelect={handleQuestion} />
        </div>

        {/* Loading state */}
        {isLoading && (
          <div className="bg-white rounded-xl border border-gray-200 p-8 text-center">
            <div className="animate-pulse space-y-3">
              <div className="h-3 bg-gray-200 rounded w-1/2 mx-auto" />
              <div className="h-3 bg-gray-200 rounded w-3/4 mx-auto" />
              <div className="h-32 bg-gray-100 rounded mt-4" />
            </div>
            <p className="text-sm text-gray-400 mt-4">
              Generating SQL and fetching data...
            </p>
          </div>
        )}

        {/* Error state */}
        {error && !isLoading && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-6">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {/* Results */}
        {result && !isLoading && (
          <div className="space-y-4">
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <ChartDisplay
                chartType={result.chart_type}
                chartData={result.chart_data}
                xKey={result.x_key}
                yKeys={result.y_keys}
                columns={result.columns}
                title={result.title}
                rowCount={result.row_count}
                message={result.message}
              />
            </div>
            <SqlDisplay sql={result.sql} />
          </div>
        )}

        {/* Empty state */}
        {!result && !isLoading && !error && (
          <div className="text-center py-16 text-gray-400">
            <p className="text-4xl mb-3">📊</p>
            <p className="text-sm">Ask a question to see your data as a chart</p>
          </div>
        )}

      </main>
    </div>
  )
}