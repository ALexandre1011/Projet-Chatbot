import random
import fasttext
import os

labels = [
    "get", "post", "delete",
    "customer_name", "customer_email", "product_purchased",
    "date_of_purchase", "ticket_description", "ticket_channel",
    "customer_satisfaction_rating", "ticket_status", "ticket_priority",
    "ticket_type", "ticket_subject", "resolution",
    "first_response_time", "time_to_resolution"
]

intent_templates = {
    "get": ["get ticket #{}", "show me ticket #{}", "retrieve ticket #{}", "i want to see ticket #{}"],
    "post": ["create ticket", "open a ticket", "submit new ticket", "start ticket"],
    "delete": ["delete ticket #{}", "remove ticket #{}", "erase ticket #{}", "cancel ticket #{}"]
}

column_templates = [
    "tell me the {} of ticket #{}",
    "what is the {} of ticket #{}",
    "i want to know the {} of ticket #{}",
    "show me the {} of ticket #{}",
    "give me the {} of ticket #{}"
]

letters = "abcdefghijklmnopqrstuvwxyz"

def generate_typos(word, max_typos=2, n=20):
    typo_variants = set()
    while len(typo_variants) < n:
        typo = list(word)
        for _ in range(max_typos):
            if not typo:
                break
            idx = random.randint(0, len(typo)-1)
            op = random.choice(["insert", "delete", "swap", "replace"])
            if op == "insert":
                typo.insert(idx, random.choice(letters))
            elif op == "delete" and len(typo) > 1:
                del typo[idx]
            elif op == "swap" and idx < len(typo) - 1:
                typo[idx], typo[idx+1] = typo[idx+1], typo[idx]
            elif op == "replace":
                typo[idx] = random.choice(letters)
        typo_word = ''.join(typo)
        if typo_word != word:
            typo_variants.add(typo_word)
    return list(typo_variants)

# Écriture du corpus
with open("corpus.txt", "w", encoding="utf-8") as f:
    # Intents
    for intent in ["get", "post", "delete"]:
        templates = intent_templates[intent]
        for _ in range(100):
            phrase = random.choice(templates).format(random.randint(1, 100))
            f.write(f"__label__{intent} {phrase}\n")

    # Champs
    for label in labels:
        if label in ["get", "post", "delete"]:
            continue
        readable = label.replace("_", " ")
        for _ in range(50):  # phrases correctes
            ticket_id = random.randint(1, 100)
            phrase = random.choice(column_templates).format(readable, ticket_id)
            f.write(f"__label__{label} {phrase}\n")

        typos = generate_typos(readable.replace(" ", ""), n=50)
        for typo in typos:
            ticket_id = random.randint(1, 100)
            phrase = random.choice(column_templates).format(typo, ticket_id)
            f.write(f"__label__{label} {phrase}\n")