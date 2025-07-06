import fasttext
from rapidfuzz import process
import re

model = fasttext.load_model("frontend/embeddings/fasttext_model.bin")


VALID_LABELS = [
    "get", "post", "delete","customer_name","customer_email","product_purchased",
    "date_of_purchase","ticket_description","ticket_channel","customer_satisfaction_rating",
    "ticket_status","ticket_priority","ticket_type","ticket_subject","resolution",
    "first_response_time","time_to_resolution"
]

def correct_label(label):
    match, score, _ = process.extractOne(label, VALID_LABELS)
    return match if score > 80 else label  

def classify_text(text):
    label, prob = model.predict(text)
    raw = label[0].replace("__label__", "")
    corrected = correct_label(raw)
    print(f"DEBUG: Prediction: {raw} (corrected to: {corrected}), Prob: {prob}")
    return corrected


def extract_id(text):
    match = re.search(r'#\s*(\d+)', text)
    return match.group(1) if match else None
