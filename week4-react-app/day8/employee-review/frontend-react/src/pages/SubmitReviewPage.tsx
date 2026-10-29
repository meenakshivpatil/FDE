import { useState, useEffect } from 'react'
import type { Employee, ReviewPeriod } from "../types"
import Header from "../components/header"
import { useNavigate } from 'react-router'

const CATEGORIES = [
  { key: 'quality_rating', label: 'Quality of Work' },
  { key: 'delivery_rating', label: 'Delivery & Ownership' },
  { key: 'teamwork_rating', label: 'Teamwork & Collaboration' },
] as const

type RatingKey = typeof CATEGORIES[number]['key']
type Ratings = Record<RatingKey, number>

const EMPTY_RATINGS: Ratings = { quality_rating: 0, delivery_rating: 0, teamwork_rating: 0 }

function formatPeriod(period: ReviewPeriod) {
  const month = (d: string) => new Date(d + 'T00:00:00').toLocaleString('en-US', { month: 'short' })
  return `${period.name} (${month(period.start_date)} - ${month(period.end_date)})`
}
// on clicking submit Review, the form data is validated and sent to the backend API
function validateForm(employeeId: string, periodId: string, ratings: Ratings, comments: string) {
  if (!employeeId || !periodId || CATEGORIES.some(c => ratings[c.key] === 0) || !comments.trim()) {
    return false
  }
  return true
}

//submit review to backend API after validation
function submitReview(employeeId: string, periodId: string, ratings: Ratings, comments: string) {
  if (!validateForm(employeeId, periodId, ratings, comments)) {
    return Promise.reject('Validation failed')
  }
  return fetch('http://127.0.0.1:8000/reviews', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      employee_id: Number(employeeId),
      period_id: Number(periodId),
      ...ratings,
      comments,
    }),
  })
}
//navigate to Review List page after successful submission


function SubmitReviewPage() {
  const [employees, setEmployees] = useState<Employee[]>([])
  const [reviewPeriods, setReviewPeriods] = useState<ReviewPeriod[]>([])
  const [employeeId, setEmployeeId] = useState('')
  const [periodId, setPeriodId] = useState('')
  const [ratings, setRatings] = useState<Ratings>(EMPTY_RATINGS)
  const [comments, setComments] = useState('')
  const [message, setMessage] = useState('')

  const navigate = useNavigate()

  // Submit the review using the current form state.
  const handleReviewSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    submitReview(employeeId, periodId, ratings, comments)
      .then(response => {
        if (!response.ok) throw new Error('Request failed')
        setMessage('Review submitted successfully.')
        navigate('/reviews')
      })
      .catch(() => setMessage('Failed to submit review.'))
  }

  useEffect(() => {
    fetch('http://127.0.0.1:8000/employees')
      .then(response => response.json())
      .then(data => setEmployees(data))
  }, [])

  useEffect(() => {
    fetch('http://127.0.0.1:8000/review-periods')
      .then(response => response.json())
      .then(data => setReviewPeriods(data))
  }, [])

  // Clicking the current rating again clears it; otherwise the first N stars are filled.
  const handleStarClick = (key: RatingKey, value: number) => {
    setRatings(prev => ({ ...prev, [key]: prev[key] === value ? 0 : value }))
  }

  const handleReset = () => {
    setEmployeeId('')
    setPeriodId('')
    setRatings(EMPTY_RATINGS)
    setComments('')
    setMessage('')
  }

  return (
    <div className="review-card">
      <Header />
      <form onSubmit={handleReviewSubmit}>
        <div className="row">
          <div className="field">
            <label htmlFor="employee">Employee <span className="req">*</span></label>
            <select id="employee" value={employeeId} onChange={e => setEmployeeId(e.target.value)}>
              <option value="">Select employee</option>
              {employees.map(employee => (
                <option key={employee.id} value={employee.id}>
                  {employee.employee_id} - {employee.name}
                </option>
              ))}
            </select>
          </div>
          <div className="field">
            <label htmlFor="period">Review Period <span className="req">*</span></label>
            <select id="period" value={periodId} onChange={e => setPeriodId(e.target.value)}>
              <option value="">Select period</option>
              {reviewPeriods.map(period => (
                <option key={period.id} value={period.id}>
                  {formatPeriod(period)}
                </option>
              ))}
            </select>
          </div>
        </div>

        <h3 className="section-title">Performance Ratings (1 - 5)</h3>
        {CATEGORIES.map(({ key, label }) => (
          <div className="rating-row" key={key}>
            <span className="rating-label">{label} <span className="req">*</span></span>
            <div className="stars">
              {[1, 2, 3, 4, 5].map(value => (
                <button
                  type="button"
                  key={value}
                  className={value <= ratings[key] ? 'star filled' : 'star'}
                  onClick={() => handleStarClick(key, value)}
                  aria-label={`${label}: ${value} star${value > 1 ? 's' : ''}`}
                >
                  ★
                </button>
              ))}
            </div>
          </div>
        ))}

        <div className="field comments">
          <label htmlFor="comments">Overall Comments <span className="req">*</span></label>
          <textarea
            id="comments"
            rows={4}
            placeholder="Enter your feedback, strengths, areas of improvement..."
            value={comments}
            onChange={e => setComments(e.target.value)}
          />
        </div>

        {message && <p className="message">{message}</p>}

        <div className="actions">
          <button type="button" className="btn secondary" onClick={handleReset}>Reset</button>
          <button type="submit" className="btn primary">Submit Review</button>
        </div>
      </form>
    </div>
  )
}

export default SubmitReviewPage
