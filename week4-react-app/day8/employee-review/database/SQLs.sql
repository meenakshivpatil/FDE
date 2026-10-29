CREATE TABLE employees (
    id          SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    name        VARCHAR(100) NOT NULL,
    department  VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NULL,
    status      VARCHAR(20) DEFAULT 'Active'
);

INSERT INTO employees (employee_id, name, department, email, status) VALUES
    ('EMP101', 'Asha Raman',    'Engineering', 'asha.raman@example.com',    'Active'),
    ('EMP102', 'Ravi Kumar',    'Engineering', 'ravi.kumar@example.com',    'Active'),
    ('EMP103', 'Meera Nair',    'Quality',     'meera.nair@example.com',    'Active'),
    ('EMP104', 'John Peters',   'Operations',  'john.peters@example.com',   'Active'),
    ('EMP105', 'Sara Thomas',   'HR',          NULL,                        'Inactive');

INSERT INTO employees (employee_id, name, department, email, status) VALUES
('EMP106', 'Fiona Gallagher', 'Marketing', 'fiona.gallagher@example.com', 'Inactive'),
('EMP107', 'George Clark', 'Engineering', 'george.clark@example.com', 'Active'),
('EMP108', 'Hannah Abbott', 'Customer Support', 'hannah.abbott@example.com', 'Active'),
('EMP109', 'Ian Malcolm', 'Research', 'ian.malcolm@example.com', 'Active'),
('EMP110', 'Julia Roberts', 'Sales', 'julia.roberts@example.com', 'Active'),
('EMP111', 'Kevin Bacon', 'Sales', 'kevin.bacon@example.com', 'Active'),
('EMP112', 'Laura Croft', 'Engineering', 'laura.croft@example.com', 'Active'),
('EMP113', 'Michael Scott', 'Management', 'michael.scott@example.com', 'Active'),
('EMP114', 'Pam Beesly', 'Human Resources', 'pam.beesly@example.com', 'Active'),
('EMP115', 'Jim Halpert', 'Sales', 'jim.halpert@example.com', 'Active'),
('EMP116', 'Dwight Schrute', 'Sales', 'dwight.schrute@example.com', 'Active'),
('EMP117', 'Angela Martin', 'Accounting', 'angela.martin@example.com', 'Active'),
('EMP118', 'Oscar Martinez', 'Accounting', 'oscar.martinez@example.com', 'Active'),
('EMP119', 'Stanley Hudson', 'Sales', 'stanley.hudson@example.com', 'Active'),
('EMP120', 'Ryan Howard', 'Management', 'ryan.howard@example.com', 'Inactive'),
('EMP121', 'Kelly Kapoor', 'Customer Support', 'kelly.kapoor@example.com', 'Active'),
('EMP122', 'Toby Flenderson', 'Human Resources', 'toby.flenderson@example.com', 'Inactive');



SELECT * FROM employees;


CREATE TABLE review_periods (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date   DATE NOT NULL,
    status     VARCHAR(20) DEFAULT 'Open'
);

INSERT INTO review_periods (name, start_date, end_date, status) VALUES
    ('H2 2025', '2025-07-01', '2025-12-31', 'Closed'),
    ('H1 2026', '2026-01-01', '2026-06-30', 'Closed'),
    ('H2 2026', '2026-07-01', '2026-12-31', 'Open');

UPDATE review_periods SET name = 'H2 2025 (Jul-Dec)' WHERE id = 1;
UPDATE review_periods SET name = 'H1 2026 (Jan-Jun)' WHERE id = 2;
UPDATE review_periods SET name = 'H2 2026 (Jul-Dec)' WHERE id = 3;





select * from review_periods;

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
    (4, 2, 3, 3, 4, 3.33, NULL);


select * from performance_reviews;


SELECT current_user;

GRANT USAGE ON SCHEMA public TO fde_user;

GRANT SELECT, INSERT, UPDATE, DELETE
ON employees, review_periods, performance_reviews
TO fde_user;

-- needed for INSERTs on SERIAL id columns
GRANT USAGE, SELECT
ON SEQUENCE employees_id_seq, review_periods_id_seq, performance_reviews_id_seq
TO fde_user;