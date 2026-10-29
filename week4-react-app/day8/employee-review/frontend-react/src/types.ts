
export interface Employee {
    id: number;
    employee_id: string;
    name: string;
    department: string;
    email: string | null;
    status: "Active" | "Inactive";
}


export interface ReviewPeriod {
    id: number;
    name: string;
    start_date: string;
    end_date: string;
    status: "Open" | "Closed";
}

export interface PerformanceReview {
    id: number;
    employee_id: number;
    period_id: number;
    quality_rating: number;
    delivery_rating: number;
    teamwork_rating: number;
    average_rating: number;
    created_at: string;
    comments: string | null;
}


