// Pagination component for navigating through patient encounters



// Props:
// - currentPage: the current page number
// - totalPages: the total number of pages
// - onPageChange: callback function to handle page changes
// Usage:
// <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={handlePageChange} />
interface PaginationProps {
    currentPage: number,
    totalPages: number,
    onPageChange: (page: number) => void
}



export default function Pagination({ currentPage, totalPages, onPageChange }: PaginationProps) {
    return (
        <div>
            <button onClick={() => onPageChange(currentPage - 1)} disabled={currentPage === 1}>
                Previous
            </button>
            <span>{currentPage} / {totalPages}</span>
            <button onClick={() => onPageChange(currentPage + 1)} disabled={currentPage === totalPages}>
                Next
            </button>
        </div>
    );
}