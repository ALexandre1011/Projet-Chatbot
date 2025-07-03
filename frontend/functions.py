from Levenshtein import distance as levenshtein_distance
import fasttext
import re 

model = fasttext.load_model("frontend/embeddings/fasttext_model.bin")

def levenshtein_similarity(a, b):
    dist = levenshtein_distance(a, b)
    max_len = max(len(a), len(b))
    similarity = (1 - dist / max_len) * 100 if max_len > 0 else 0
    return dist, similarity

def sentence_similarity(a, b):
    def vectorize(word):
        try:
            return model.get_word_vector(word)
        except Exception:
            return None

    a_words = [vectorize(w) for w in a.lower().split()]
    b_words = [vectorize(w) for w in b.lower().split()]

    a_vecs = [v for v in a_words if v is not None]
    b_vecs = [v for v in b_words if v is not None]

    if not a_vecs or not b_vecs:
        return 0

    import numpy as np
    a_mean = np.mean(a_vecs, axis=0)
    b_mean = np.mean(b_vecs, axis=0)

    similarity = np.dot(a_mean, b_mean) / (np.linalg.norm(a_mean) * np.linalg.norm(b_mean))
    return round(similarity * 100, 2)

COMMAND_KEYWORDS = {
    "get": "get",
    "delete": "delete",
    "create": "create",
    "post":"create"
}

COLUMN_KEYWORDS = {
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

def correct_command(text):
    words = text.lower().split()
    best = None
    best_score = 0
    for word in words:
        for key, cmd in COMMAND_KEYWORDS.items():
            dist, sim = levenshtein_similarity(word, key)
            sem = sentence_similarity(word, key)
            if dist <= 2 and sem >= 80:
                if sem > best_score:
                    best, best_score = cmd, sem
                if dist == 0 and sem == 100:
                    return best
    return best

def correct_column_request(text):
    text = text.lower()
    best_col = None
    best_score = 0

    for label, col_name in COLUMN_KEYWORDS.items():
        label = label.lower()
        dist, lev_sim = levenshtein_similarity(text, label)
        sem_sim = sentence_similarity(text, label)

        label_words = label.split()
        if all(word in text for word in label_words):
            sem_sim += 10 
        if lev_sim >= 40 or sem_sim >= 55:
            score = (lev_sim + sem_sim) / 2
            if score > best_score:
                best_score = score
                best_col = col_name

    return best_col

def extract_id(text):
    matche = re.search(r'#\s*(\d+)', text)
    return matche.group(1)
