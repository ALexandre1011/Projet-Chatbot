import fasttext

keywords = [
    "status", "channel", "satisfaction", "priority", "resolution",
    "type", "subject", "description", "email", "name", "purchase",
    "product", "gender", "age", "create", "delete"
]
typo_variants = {
    "channel": ["chanell", "chanal", "chnnel", "chanel"],  
    "status": ["statu", "stauts", "staus"],
    "priority": ["prioritty", "prioriy"],
}
with open("corpus.txt", "w") as f:
    for word in keywords:
        for i in range(40):
            f.write(f"{word} of ID\n")
            f.write(f"get {word} of ticket\n")
            f.write(f"show me the {word}\n")
            f.write(f"{word}\n")

    for correct_word, typos in typo_variants.items():
        for typo in typos:
            for i in range(20):
                f.write(f"{typo} means {correct_word}\n")
                f.write(f"{typo} refers to {correct_word}\n")
                f.write(f"{correct_word} also written as {typo}\n")

model = fasttext.train_unsupervised("corpus.txt", model='skipgram')
model.save_model("frontend/embeddings/fasttext_model.bin")