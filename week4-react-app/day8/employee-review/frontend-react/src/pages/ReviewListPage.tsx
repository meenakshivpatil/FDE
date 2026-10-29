import { useNavigate } from 'react-router'
import { useEffect, useState } from 'react'
import type { Employee, PerformanceReview, ReviewPeriod } from '../types'
import Pagination from '../components/pagination'

const PAGE_SIZE = 5

// The /reviews API returns all reviews with numeric employee/period ids,
// so names are joined in here and filtering is done on the client.
function ReviewListPage() {
  const [reviews, setReviews] = useState<PerformanceReview[]>([])
  const [employees, setEmployees] = useState<Employee[]>([])
  const [reviewPeriods, setReviewPeriods] = useState<ReviewPeriod[]>([])
  const [selectedEmployee, setSelectedEmployee] = useState('')
  const [selectedReviewPeriod, setSelectedReviewPeriod] = useState('')
  // Filters only take effect when Search is clicked
  const [filters, setFilters] = useState({ employee: '', period: '' })
  const [page, setPage] = useState(1)
  const navigate = useNavigate()

  useEffect(() => {
    fetch('http://127.0.0.1:8000/employees')
      .then(res => res.json())
      .then(data => setEmployees(data))
    fetch('http://127.0.0.1:8000/review-periods')
      .then(res => res.json())
      .then(data => setReviewPeriods(data))
    fetch('http://127.0.0.1:8000/reviews')
      .then(res => res.json())
      .then(data => setReviews(data))
  }, [])

  const handleSearch = () => {
    setFilters({ employee: selectedEmployee, period: selectedReviewPeriod })
    setPage(1)
  }

  const filtered = reviews.filter(review =>
    (!filters.employee || review.employee_id === Number(filters.employee)) &&
    (!filters.period || review.period_id === Number(filters.period))
  )
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const start = (page - 1) * PAGE_SIZE
  const pageRows = filtered.slice(start, start + PAGE_SIZE)

  const employeeById = new Map(employees.map(e => [e.id, e]))
  const periodById = new Map(reviewPeriods.map(p => [p.id, p]))

  const openReview = (id: number) => navigate(`/reviews/${id}`)

  return (
    <div className="review-card">
      <h2 className="page-title">Performance Reviews</h2>

      <div className="filters">
        <div className="field">
          <label htmlFor="period">Review Period</label>
          <select id="period" value={selectedReviewPeriod} onChange={e => setSelectedReviewPeriod(e.target.value)}>
            <option value="">All Periods</option>
            {reviewPeriods.map(period => (
              <option key={period.id} value={period.id}>{period.name}</option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="employee">Employee <span className="req">*</span></label>
          <select id="employee" value={selectedEmployee} onChange={e => setSelectedEmployee(e.target.value)}>
            <option value="">All Employees</option>
            {employees.map(employee => (
              <option key={employee.id} value={employee.id}>{employee.name}</option>
            ))}
          </select>
        </div>
        <button type="button" className="btn primary search-btn" onClick={handleSearch}>
          <span aria-hidden="true">⌕</span> Search
        </button>
      </div>

      <div className="table-wrap">
        <table className="review-table">
          <thead>
            <tr>
              <th>Employee ID</th>
              <th>Employee Name</th>
              <th>Period</th>
              <th className="center">Ratings</th>
              <th className="center">Average</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {pageRows.map(review => {
              const employee = employeeById.get(review.employee_id)
              const period = periodById.get(review.period_id)
              const average = (review.quality_rating + review.delivery_rating + review.teamwork_rating) / 3
              return (
                <tr key={review.id}>
                  <td>{employee?.employee_id ?? review.employee_id}</td>
                  <td>{employee?.name ?? '-'}</td>
                  <td>{period?.name ?? '-'}</td>
                  <td className="center">
                    {[review.quality_rating, review.delivery_rating, review.teamwork_rating].join(', ')}
                  </td>
                  <td className="center">{average.toFixed(1)}</td>
                  <td><span className="status-pill">Completed</span></td>
                  <td>
                    <button type="button" className="link-btn" onClick={() => openReview(review.id)}>View</button>
                  </td>
                </tr>
              )
            })}
            {pageRows.length === 0 && (
              <tr>
                <td colSpan={7} className="empty">No reviews found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="table-footer">
        <span className="showing">
          {filtered.length === 0
            ? 'Showing 0 reviews'
            : `Showing ${start + 1} to ${start + pageRows.length} of ${filtered.length} reviews`}
        </span>
        <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />
      </div>
    </div>
  )
}

export default ReviewListPage
