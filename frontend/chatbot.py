from fastapi import FastAPI
from frontend.models import UserInput
from frontend.functions import extract_id, correct_command, correct_column_request
from frontend.api import get_ticket, get_ticket_field, delete_ticket, create_ticket
from frontend.preprocessing import preprocess_text

app = FastAPI()

@app.post("/chat")
def chat(user_input: UserInput):
    raw_text = user_input.message
    ticket_id = extract_id(raw_text)
    command = correct_command(raw_text)
    processed_text = preprocess_text(raw_text)
    column_request = correct_column_request(processed_text)

    if column_request and ticket_id:
        value = get_ticket_field(ticket_id, column_request)
        if isinstance(value, str):
            return {"response": value}
        champ_valeur = value.get(column_request)
        if champ_valeur == "Champ introuvable":
            return {"response": f"The field '{column_request}' does not exist in ticket #{ticket_id}"}
        return {"response": f"The field '{column_request}' of ticket #{ticket_id} is: {champ_valeur}"}

    if not command:
        return {"response": "Sorry, I didn't understand the command."}

    # GET
    if command == "get" and ticket_id:
        ticket = get_ticket(ticket_id)
        if isinstance(ticket, str):
            return {"response": ticket}
        msg = f"Ticket #{ticket_id}:\n"
        for key, value in ticket.items():
            msg += f"- {key.replace('_', ' ').capitalize()} : {value}\n"
        return {"response": msg}

    # DELETE
    elif command == "delete" and ticket_id:
        deletion_response = delete_ticket(ticket_id)
        return {"response": deletion_response}

    # CREATE
    elif command == "create":
        data = {
            "ticket_id": ticket_id ,
            "customer_name": "Créé via le chatbot",
            "customer_email": "Créé via le chatbot",
            "product_purchased": "Créé via le chatbot",
            "date_of_purchase": "Créé via le chatbot",
            "ticket_description": "Créé via le chatbot",
            "ticket_channel": "Créé via le chatbot",
            "customer_satisfaction_rating": 0.0,
            "ticket_status": "Créé via le chatbot",
            "ticket_priority": "Créé via le chatbot",
            "ticket_type": "Créé via le chatbot",
            "ticket_subject": "Créé via le chatbot",
            "resolution": "Créé via le chatbot",
            "first_response_time": "Créé via le chatbot",
            "time_to_resolution": "Créé via le chatbot"
        }
        creation_response = create_ticket(data)
        return {"response": creation_response}

    else:
        return {"response": "Impossible to execute the command. Check format or ticket ID."}
