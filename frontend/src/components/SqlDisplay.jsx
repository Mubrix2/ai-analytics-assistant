// frontend/src/components/SqlDisplay.jsx
import { useState } from 'react'

export default function SqlDisplay({ sql }) {
  const [isOpen, setIsOpen] = useState(false)

  if (!sql) return null

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-4 py-2 
                   bg-gray-50 hover:bg-gray-100 transition-colors text-sm"
      >
        <span className="font-mono text-gray-600 font-medium">
          Generated SQL
        </span>
        <span className="text-gray-400">{isOpen ? '▲' : '▼'}</span>
      </button>

      {isOpen && (
        <pre className="px-4 py-3 text-xs font-mono text-green-700 
                        bg-gray-900 overflow-x-auto whitespace-pre-wrap">
          {sql}
        </pre>
      )}
    </div>
  )
}