#cdfrom psycopg2.extras import RealDictCursor, execute_values

from database import get_db_connection

BATCH_SIZE = 5000

def get_employees():
    conn = get_db_connection()
    conn.execute("SELECT * FROM employees")
    employees = conn.fetchall()
    return employees

def get_review_periods():
    conn = get_db_connection()
    conn.execute("SELECT * FROM review_periods")
    review_periods = conn.fetchall()
    return review_periods

def get_performance_reviews():
    conn = get_db_connection()
    conn.execute("SELECT * FROM performance_reviews")
    performance_reviews = conn.fetchall()
    return performance_reviews  

def get_performance_review(review_id: int):
    conn = get_db_connection()
    conn.execute("SELECT * FROM performance_reviews WHERE id = %s", (review_id,))
    performance_review = conn.fetchone()
    return performance_review  

def create_performance_review(review, average_rating):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO performance_reviews (employee_id, period_id, quality_rating, delivery_rating, teamwork_rating, average_rating, comments) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (review.employee_id, review.period_id, review.quality_rating, review.delivery_rating, review.teamwork_rating, average_rating, review.comments)
    )
    conn.execute("SELECT * FROM performance_reviews WHERE id = currval('performance_reviews_id_seq')")  
    new_review = conn.fetchone()
    # Commit the transaction to save the new review
    conn.connection.commit()
    return new_review