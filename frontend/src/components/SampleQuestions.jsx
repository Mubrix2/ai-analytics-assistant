// frontend/src/components/SampleQuestions.jsx

// Props:
// - questions: array of {question, description} from the API
// - onSelect: function called when user clicks a question

export default function SampleQuestions({ questions, onSelect }) {
  if (!questions || questions.length === 0) return null

  return (
    <div>
      <p className="text-xs text-gray-500 mb-2 font-medium uppercase tracking-wide">
        Try these
      </p>
      <div className="flex flex-wrap gap-2">
        {questions.map((item, index) => (
          <button
            key={index}
            onClick={() => onSelect(item.question)}
            title={item.description}
            className="px-3 py-1.5 text-xs bg-gray-100 hover:bg-blue-50 
                       hover:text-blue-700 border border-gray-200 hover:border-blue-300
                       rounded-full transition-colors cursor-pointer"
          >
            {item.question}
          </button>
        ))}
      </div>
    </div>
  )
}