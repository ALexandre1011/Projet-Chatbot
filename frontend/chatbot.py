from fastapi import FastAPI
from frontend.models import UserInput
from frontend.functions import extract_id, classify_text
from frontend.api import get_ticket, get_ticket_field, delete_ticket, create_ticket
from frontend.preprocessing import preprocess_text

app = FastAPI()

@app.post("/chat")
def chat(user_input: UserInput):
    raw_text = user_input.message
    processed_text = preprocess_text(raw_text)

    predicted_label = classify_text(processed_text)
    ticket_id = extract_id(raw_text)

    # Cas 1 : commande principale (get, post, delete)
    if predicted_label in ["get", "post", "delete"]:
        command = predicted_label

        if command == "get" and ticket_id:
            ticket = get_ticket(ticket_id)
            if isinstance(ticket, str):
                return {"response": ticket}
            msg = f"Ticket #{ticket_id}:\n"
            for key, value in ticket.items():
                msg += f"- {key.replace('_', ' ').capitalize()} : {value}\n"
            return {"response": msg}

        elif command == "delete" and ticket_id:
            deletion_response = delete_ticket(ticket_id)
            return {"response": deletion_response}

        elif command == "post":
            data = {
                "ticket_id": ticket_id,
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
            return {"response": "Please provide a valid ticket ID for this command."}

    # Cas 2 : demande d’un champ spécifique
    elif predicted_label in [
        "customer_name", "customer_email", "product_purchased", "date_of_purchase",
        "ticket_description", "ticket_channel", "customer_satisfaction_rating",
        "ticket_status", "ticket_priority", "ticket_type", "ticket_subject", "resolution",
        "first_response_time", "time_to_resolution"
    ]:
        if not ticket_id:
            return {"response": "Please provide the ticket ID (e.g., #12) to retrieve this information."}
        value = get_ticket_field(ticket_id, predicted_label)

        if "error" in value:
            return {"response": value["error"]}

        champ_valeur = value.get(predicted_label)
        if champ_valeur == "Champ introuvable":
            return {"response": f"The field '{predicted_label}' does not exist in ticket #{ticket_id}"}

        return {"response": f"The field '{predicted_label}' of ticket #{ticket_id} is: {champ_valeur}"}


    else:
        return {"response": "Sorry, I couldn't understand your request."}
