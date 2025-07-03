from sqlalchemy import Column, Integer, String, Float, Boolean
from backend.configuration import Base

class customer_ticket(Base):
    __tablename__ = "customer_tickets"
    ticket_id = Column(Integer, primary_key=True)
    customer_name = Column(String(100))
    customer_email = Column(String(100))
    product_purchased = Column(String(100))
    date_of_purchase = Column(String(100))
    ticket_type = Column(String(50))
    ticket_subject = Column(String(200))
    ticket_description = Column(String(500))
    ticket_status = Column(String(50))
    resolution = Column(String(100))
    ticket_priority = Column(String(50))
    ticket_channel = Column(String(50))
    first_response_time = Column(String(100))
    time_to_resolution = Column(String(100))
    customer_satisfaction_rating = Column(Float)
    is_deleted = Column(Boolean, default=False)
