from pydantic import BaseModel

class ticketCreate(BaseModel):
    ticket_id: int
    customer_name: str
    customer_email: str
    product_purchased: str
    date_of_purchase: str
    ticket_type: str
    ticket_subject: str
    ticket_description: str
    ticket_status: str
    resolution: str
    ticket_priority: str
    ticket_channel: str
    first_response_time: str
    time_to_resolution: str
    customer_satisfaction_rating: float

class ticketResponse(ticketCreate):
    class Config:
        orm_mode = True
