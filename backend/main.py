from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.configuration import SessionLocal
from backend.models import customer_ticket
from backend.schemas import ticketResponse, ticketCreate 

app = FastAPI()

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

@app.get("/ticket/{ticket_id}", response_model=ticketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(customer_ticket).filter(customer_ticket.ticket_id == ticket_id).first()
    if not ticket or ticket.is_deleted:
        raise HTTPException(status_code=404, detail=f"Ticket #{ticket_id} does not exist")
    return ticket

@app.post("/ticket")
def create_ticket(ticket_data: ticketCreate, db: Session = Depends(get_db)):
    existing_ticket = db.query(customer_ticket).filter(customer_ticket.ticket_id == ticket_data.ticket_id).first()
    if existing_ticket:
        if not existing_ticket.is_deleted:
            raise HTTPException(status_code=400, detail=f"The ticket #{ticket_data.ticket_id} already exist")
        
        existing_ticket.is_deleted = False
        db.commit()
        return {"message": f"The ticket #{ticket_data.ticket_id} has been recreated"}
    
    new_ticket = customer_ticket(**ticket_data.model_dump(), is_deleted=False)
    db.add(new_ticket)
    db.commit()
    return {"message": f"The ticket #{ticket_data.ticket_id} has been created"}

@app.delete("/ticket/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(customer_ticket).filter(customer_ticket.ticket_id == ticket_id).first()
    if not ticket or ticket.is_deleted:
        raise HTTPException(status_code=404, detail=f"The ticket #{ticket_id} does not exist")
    ticket.is_deleted = True
    db.commit()
    return {"message": f"The ticket #{ticket_id} has been deleted"}