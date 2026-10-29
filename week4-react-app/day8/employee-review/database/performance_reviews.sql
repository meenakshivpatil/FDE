CREATE TABLE performance_reviews (
    id              SERIAL PRIMARY KEY,
    employee_id     INTEGER NOT NULL REFERENCES employees(id),
    period_id       INTEGER NOT NULL REFERENCES review_periods(id),
    quality_rating  INTEGER NOT NULL CHECK (quality_rating BETWEEN 1 AND 5),
    delivery_rating INTEGER NOT NULL CHECK (delivery_rating BETWEEN 1 AND 5),
    teamwork_rating INTEGER NOT NULL CHECK (teamwork_rating BETWEEN 1 AND 5),
    average_rating  DECIMAL(3,2) NOT NULL,
    comments        TEXT NULL,
    created_at      TIMESTAMP DEFAULT NOW()
);

INSERT INTO performance_reviews
    (employee_id, period_id, quality_rating, delivery_rating, teamwork_rating, average_rating, comments) VALUES
    (1, 1, 4, 5, 4, 4.33, 'Consistently delivers on time.'),
    (1, 2, 5, 5, 4, 4.67, 'Strong technical leadership.'),
    (2, 1, 3, 4, 4, 3.67, 'Good progress; improve code quality.'),
    (2, 2, 4, 4, 5, 4.33, 'Great team collaborator.'),
    (3, 2, 5, 4, 5, 4.67, 'Excellent attention to detail.'),
    (4, 2, 3, 3, 4, 3.33, NULL),
    (5, 3, 4, 4, 5, 4.33, 'Strong HR support.'),
    (1, 3, 5, 5, 5, 5.00, 'Outstanding performance.'),
    (2, 3, 4, 4, 4, 4.00, 'Consistent performer.'),
    (3, 3, 5, 5, 5, 5.00, 'Exceptional quality and teamwork.'),
    (4, 3, 4, 4, 4, 4.00, 'Solid performance.'),
    (5, 3, 4, 4, 4, 4.00, 'Consistent HR support.'),
    (1, 4, 5, 5, 5, 5.00, 'Outstanding performance in the new period.'),
    (2, 4, 4, 4, 4, 4.00, 'Consistent performer in the new period.'),
    (3, 4, 5, 5, 5, 5.00, 'Exceptional quality and teamwork in the new period.'),
    (4, 4, 4, 4, 4, 4.00, 'Solid performance in the new period.'),
    (5, 4, 4, 4, 4, 4.00, 'Consistent HR support in the new period.'),
    (1, 5, 5, 5, 5, 5.00, 'Outstanding performance in the latest period.'),
    (2, 5, 4, 4, 4, 4.00, 'Consistent performer in the latest period.'),
    (3, 5, 5, 5, 5, 5.00, 'Exceptional quality and teamwork in the latest period.'),
    (4, 5, 4, 4, 4, 4.00, 'Solid performance in the latest period.'),
    (5, 5, 4, 4, 4, 4.00, 'Consistent HR support in the latest period.');
    