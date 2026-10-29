import repository
from models import Employee, review_period, performance_review
def get_employees():
    # Implement the logic to fetch employees from the database
    return repository.get_employees()

def get_review_periods():
    # Implement the logic to fetch review periods from the database
    return repository.get_review_periods()

def get_performance_reviews():
    # Implement the logic to fetch performance reviews from the database
    return repository.get_performance_reviews()

def get_performance_review(review_id: int):
    # Implement the logic to fetch a single performance review by ID from the database
    return repository.get_performance_review(review_id)

def create_performance_review(review):
    # Implement the logic to create a new performance review in the database
    #calculate Average rating = (quality+delivery+teamwork) / 3
    print("Creating performance review:", review)
    average_rating = (review.quality_rating + review.delivery_rating + review.teamwork_rating) / 3
    print("Calculated average rating:", average_rating)
    return repository.create_performance_review(review, average_rating)