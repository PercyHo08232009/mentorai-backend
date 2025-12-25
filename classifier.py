from transformers import pipeline

classifier = pipeline("zero-shot-classification", model = "facebook/bart-large-mnli")

LABELS = [
    "learning question",
    "casual conversation",
    "homework cheating",
    "off topic"
]

def is_supported_question(text: str) -> bool:
    result = classifier(text, LABELS)
    top_label = result["labels"][0]
    return top_label == "learning question"