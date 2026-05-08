// frontend/src/components/QueryInput.jsx
import { useState } from 'react'

export default function QueryInput({ onSubmit, isLoading }) {
  const [question, setQuestion] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    if (question.trim()) {
      onSubmit(question)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about your sales data..."
        disabled={isLoading}
        className="flex-1 px-4 py-3 border border-gray-300 rounded-lg 
                   focus:outline-none focus:ring-2 focus:ring-blue-500
                   disabled:bg-gray-100 text-sm"
      />
      <button
        type="submit"
        disabled={isLoading || !question.trim()}
        className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium
                   hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed
                   transition-colors text-sm"
      >
        {isLoading ? 'Thinking...' : 'Ask'}
      </button>
    </form>
  )
}