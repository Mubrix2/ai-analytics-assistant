// frontend/src/components/ChartDisplay.jsx
import {
  BarChart, Bar,
  LineChart, Line,
  PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid,
  Tooltip, Legend,
  ResponsiveContainer,
} from 'recharts'

// Colours for pie chart slices and bars
const COLORS = [
  '#3b82f6', '#10b981', '#f59e0b',
  '#ef4444', '#8b5cf6', '#06b6d4',
  '#84cc16', '#f97316',
]

// Format large numbers for axis labels e.g. 5000000 → "5M"
function formatNumber(value) {
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`
  if (value >= 1_000) return `${(value / 1_000).toFixed(0)}K`
  return value
}

function renderBarChart(data, xKey, yKeys) {
  return (
    <BarChart data={data}>
      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
      <XAxis
        dataKey={xKey}
        tick={{ fontSize: 11 }}
        angle={-30}
        textAnchor="end"
        height={60}
      />
      <YAxis tickFormatter={formatNumber} tick={{ fontSize: 11 }} />
      <Tooltip formatter={(value) => value.toLocaleString()} />
      <Legend />
      {yKeys.map((key, i) => (
        <Bar key={key} dataKey={key} fill={COLORS[i % COLORS.length]} radius={[4, 4, 0, 0]} />
      ))}
    </BarChart>
  )
}

function renderLineChart(data, xKey, yKeys) {
  return (
    <LineChart data={data}>
      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
      <XAxis dataKey={xKey} tick={{ fontSize: 11 }} angle={-30} textAnchor="end" height={60} />
      <YAxis tickFormatter={formatNumber} tick={{ fontSize: 11 }} />
      <Tooltip formatter={(value) => value.toLocaleString()} />
      <Legend />
      {yKeys.map((key, i) => (
        <Line
          key={key}
          type="monotone"
          dataKey={key}
          stroke={COLORS[i % COLORS.length]}
          strokeWidth={2}
          dot={false}
        />
      ))}
    </LineChart>
  )
}

function renderPieChart(data, xKey, yKeys) {
  const valueKey = yKeys[0]
  return (
    <PieChart>
      <Pie
        data={data}
        dataKey={valueKey}
        nameKey={xKey}
        cx="50%"
        cy="50%"
        outerRadius={140}
        label={({ name, percent }) =>
          `${name} ${(percent * 100).toFixed(1)}%`
        }
      >
        {data.map((_, index) => (
          <Cell key={index} fill={COLORS[index % COLORS.length]} />
        ))}
      </Pie>
      <Tooltip formatter={(value) => value.toLocaleString()} />
    </PieChart>
  )
}

function renderTable(data, columns) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="bg-gray-50">
            {columns.map((col) => (
              <th key={col} className="px-4 py-2 text-left font-medium text-gray-600 
                                       border-b border-gray-200">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className="hover:bg-gray-50 border-b border-gray-100">
              {columns.map((col) => (
                <td key={col} className="px-4 py-2 text-gray-700">
                  {typeof row[col] === 'number'
                    ? row[col].toLocaleString()
                    : row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

// Props:
// - chartType: string from API — "bar", "line", "pie", "table", "empty", "error"
// - chartData: array of data objects
// - xKey: which field is the x-axis/label
// - yKeys: which fields are the values
// - columns: all column names (used for table)
// - title: the original question
// - rowCount: total rows
// - message: error or info message from API

export default function ChartDisplay({
  chartType, chartData, xKey, yKeys,
  columns, title, rowCount, message
}) {
  if (chartType === 'error' || message) {
    return (
      <div className="p-6 bg-amber-50 border border-amber-200 rounded-lg text-center">
        <p className="text-amber-700">{message || 'Could not generate a chart for this query.'}</p>
      </div>
    )
  }

  if (chartType === 'empty' || !chartData || chartData.length === 0) {
    return (
      <div className="p-6 bg-gray-50 border border-gray-200 rounded-lg text-center">
        <p className="text-gray-500">No data returned for this question.</p>
      </div>
    )
  }

  const chartContent = {
    bar: () => renderBarChart(chartData, xKey, yKeys),
    line: () => renderLineChart(chartData, xKey, yKeys),
    pie: () => renderPieChart(chartData, xKey, yKeys),
    table: () => renderTable(chartData, columns),
  }[chartType]?.()

  if (!chartContent) return null

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-gray-700">{title}</h3>
        <span className="text-xs text-gray-400">{rowCount} rows</span>
      </div>

      {chartType === 'table' ? (
        chartContent
      ) : (
        <ResponsiveContainer width="100%" height={350}>
          {chartContent}
        </ResponsiveContainer>
      )}
    </div>
  )
}