import { Link, useParams } from 'react-router'
import { useEffect, useState } from 'react'
import type { Employee, PerformanceReview, ReviewPeriod } from '../types'

// The review API only returns employee/period ids, so the names are
// looked up from the employees and review-periods lists.

function formatPeriod(period: ReviewPeriod) {
  const month = (d: string) => new Date(d + 'T00:00:00').toLocaleString('en-US', { month: 'short' })
  return `${period.name} (${month(period.start_date)} - ${month(period.end_date)})`
}

function ReviewDetailsPage() {
  // ":id" from the route path /reviews/:id
  const { id } = useParams()

  const [review, setReview] = useState<PerformanceReview | null>(null)
  const [employees, setEmployees] = useState<Employee[]>([])
  const [reviewPeriods, setReviewPeriods] = useState<ReviewPeriod[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    if (id) {
      fetch(`http://127.0.0.1:8000/reviews/${id}`)
        .then(res => {
          if (!res.ok) throw new Error('Request failed')
          return res.json()
        })
        .then(data => setReview(data))
        .catch(() => setError('Review not found.'))
    }
  }, [id])

  useEffect(() => {
    fetch('http://127.0.0.1:8000/employees')
      .then(res => res.json())
      .then(data => setEmployees(data))
    fetch('http://127.0.0.1:8000/review-periods')
      .then(res => res.json())
      .then(data => setReviewPeriods(data))
  }, [])

  const employee = employees.find(e => e.id === review?.employee_id)
  const period = reviewPeriods.find(p => p.id === review?.period_id)

  const criteria = review
    ? [
        { name: 'Quality of Work', rating: review.quality_rating },
        { name: 'Delivery & Ownership', rating: review.delivery_rating },
        { name: 'Teamwork & Collaboration', rating: review.teamwork_rating },
      ]
    : []

  return (
    <div className="review-card">
      <div className="details-header">
        <h2 className="page-title">Review Details</h2>
        <Link to="/reviews" className="btn outline">Back to List</Link>
      </div>

      {error && <p className="message">{error}</p>}
      {!review && !error && <p className="message">Loading...</p>}

      {review && (
        <>
          <div className="summary-grid">
            <div className="summary-box">
              <span className="summary-label">Employee</span>
              <span>{employee ? `${employee.employee_id} - ${employee.name}` : '-'}</span>
            </div>
            <div className="summary-box">
              <span className="summary-label">Review Period</span>
              <span>{period ? formatPeriod(period) : '-'}</span>
            </div>
            <div className="summary-box">
              <span className="summary-label">Overall Rating</span>
              <div className="overall-rating">
                <strong>{Number(review.average_rating).toFixed(1)}</strong> / 5
              </div>
            </div>
          </div>

          <h3 className="section-title">Performance Criteria</h3>
          <div className="table-wrap">
            <table className="review-table criteria-table">
              <thead>
                <tr>
                  <th>Criteria</th>
                  <th>Rating</th>
                </tr>
              </thead>
              <tbody>
                {criteria.map(criterion => (
                  <tr key={criterion.name}>
                    <td>{criterion.name}</td>
                    <td>
                      <span className="stars" aria-label={`${criterion.rating} out of 5`}>
                        {[1, 2, 3, 4, 5].map(value => (
                          <span key={value} className={value <= criterion.rating ? 'star filled' : 'star'}>★</span>
                        ))}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <h3 className="section-title">Manager Comments</h3>
          <div className="comments-box">{review.comments || 'No comments.'}</div>
        </>
      )}
    </div>
  )
}

export default ReviewDetailsPage
