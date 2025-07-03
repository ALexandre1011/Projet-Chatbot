import streamlit as st
import requests

# URL de l'API FastAPI
API_URL = "http://localhost:8002/chat"

st.set_page_config(page_title="Chatbot Support", page_icon="💬")

st.title("💬 Service Client - Chatbot")

st.markdown("Posez une question sur un ticket client")

# Stocker l'historique des messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Entrée utilisateur
user_message = st.chat_input("Votre message :", key="user_input")

# Lorsqu'on appuie sur Entrée
if user_message:
    # Ajouter le message utilisateur à l'historique
    st.session_state.chat_history.append({"role": "user", "content": user_message})

    # Appeler l’API FastAPI
    try:
        response = requests.post(API_URL, json={"message": user_message})
        if response.status_code == 200:
            bot_response = response.json().get("response", "Réponse vide")
        else:
            bot_response = f"Erreur {response.status_code}: {response.text}"
    except Exception as e:
        bot_response = f"Erreur lors de l'appel API : {str(e)}"

    # Ajouter la réponse du bot à l'historique

    st.session_state.chat_history.append({"role": "ai", "content": bot_response})

# Affichage de la conversation
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
