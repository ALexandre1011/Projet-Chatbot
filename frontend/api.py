import requests

BASE_URL = "http://localhost:8001"

def ticket_exists(ticket_id):
    res = requests.get(f"{BASE_URL}/ticket/{ticket_id}")
    return res.status_code == 200

def create_ticket(data):
    try:
        response = requests.post(f"{BASE_URL}/ticket", json=data)
        if response.status_code == 400:
            return response.json().get("detail", "Ticket exists")
        return response.json().get("message", "Unknown response")
    except Exception as e:
        return f"Error creating ticket: {str(e)}"

def get_ticket(ticket_id):
    try:
        response = requests.get(f"{BASE_URL}/ticket/{ticket_id}")
        if response.status_code == 404:
            return f"The ticket #{ticket_id} does not exist"
        return response.json()
    except Exception as e:
        return f"Error fetching ticket: {str(e)}"

def delete_ticket(ticket_id):
    try:
        response = requests.delete(f"{BASE_URL}/ticket/{ticket_id}")
        if response.status_code == 404:
            return f"The ticket #{ticket_id} does not exist"
        return response.json().get("message", f"The ticket #{ticket_id} has been deleted")
    except Exception as e:
        return f"Error deleting ticket: {str(e)}"


def get_ticket_field(ticket_id, field):
    if not ticket_exists(ticket_id):
        return f"The ticket #{ticket_id} does not exist"
    res = requests.get(f"{BASE_URL}/ticket/{ticket_id}")
    ticket = res.json()
    return {field: ticket.get(field, "Champ introuvable")}