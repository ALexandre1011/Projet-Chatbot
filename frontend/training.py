import random
import fasttext

intent_labels = ["get", "post", "delete"]
column_keywords = {
    "customer name":"customer_name",
    "customer email":"customer_email",
    "product":"product_purchased",
    "date of purchase":"date_of_purchase",
    "description":"ticket_description",
    "channel": "ticket_channel",
    "satisfaction rating": "customer_satisfaction_rating",
    "status": "ticket_status",
    "priority": "ticket_priority",
    "type": "ticket_type",
    "subject": "ticket_subject",
    "resolution": "resolution",
    "first response time": "first_response_time",
    "time to resolution": "time_to_resolution"
}

intent_templates = {
    "get": ["get ticket #{id}", "show ticket {id}", "retrieve ticket {id}", "I want to see ticket {id}"],
    "post": ["create ticket", "submit a new ticket", "post ticket", "add ticket"],
    "delete": ["delete ticket #{id}", "remove ticket {id}", "please delete ticket", "erase ticket"]
}

column_templates = [
    "what is the {col}?",
    "tell me the {col}",
    "show the {col}",
    "I want to know the {col}",
    "please provide {col}"
]

with open("corpus.txt", "w", encoding="utf-8") as f:
    # Intent samples
    for intent in intent_labels:
        for _ in range(100):
            example = random.choice(intent_templates[intent]).format(id=random.randint(1, 100))
            f.write(f"__label__{intent} {example}\n")

    # Column samples
    for label in column_keywords:
        col = column_keywords[label]
        for _ in range(50):
            sentence = random.choice(column_templates).format(col=label)
            f.write(f"__label__{col} {sentence}\n")


model = fasttext.train_supervised("corpus.txt", epoch=30, lr=1.0)
model.save_model("frontend/embeddings/fasttext_model.bin")