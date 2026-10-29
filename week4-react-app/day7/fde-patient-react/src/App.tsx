import { useState, useEffect} from 'react'
import type { Encounter } from "./types"
import './App.css'
import Header from "./components/Header"

import PatientTable from "./components/PatientTable"
import Pagination from './components/Pagination'

// API call should include pagination parameters (limit and offset) based on the current page

function App() {
  const [encounters, setEncounters] = useState<Encounter[]>([])
  const [currentPage, setCurrentPage] = useState(1)
  const limit = 10
  useEffect(() => {
    const offset = (currentPage - 1) * limit
    fetch(`http://127.0.0.1:8000/encounters?limit=${limit}&offset=${offset}`)
      .then(response => response.json())
      .then(data => setEncounters(data))
  }, [currentPage])

  return (
    <div>
      <Header />
      <PatientTable encounters={encounters} />
      <Pagination
        currentPage={currentPage}
        totalPages={10}
        onPageChange={(page) => setCurrentPage(page)}
      />
    </div>
  )
}

export default App
