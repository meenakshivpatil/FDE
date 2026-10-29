import { Routes, Route, Navigate } from "react-router"
import Menu from "./components/menu"
import SubmitReviewPage from "./pages/SubmitReviewPage"
import ReviewListPage from "./pages/ReviewListPage"
import ReviewDetailsPage from "./pages/ReviewDetailsPage"
import './App.css'

function App() {
  return (
    <div className="app-layout">
      <Menu />
      <main className="content">
        <Routes>
          <Route path="/submit-review" element={<SubmitReviewPage />} />
          <Route path="/reviews" element={<ReviewListPage />} />
          <Route path="/reviews/:id" element={<ReviewDetailsPage />} />
          {/* Any unknown URL (including "/") goes to the submit form */}
          <Route path="*" element={<Navigate to="/submit-review" replace />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
