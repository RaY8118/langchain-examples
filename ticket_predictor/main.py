from langchain_ollama import OllamaEmbeddings
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import numpy as np
import pandas as pd

# df = pd.read_csv("data.csv")
# description = df["description"].tolist()
# priority = df["priority"].tolist()

description = [
    # Critical Outages (Company-wide, system down)
    "VPN not working for remote employees",
    "Email service down company wide",
    "Production database cluster is completely unresponsive",
    "Active Directory server crashed, no one can log in",

    # High Impact (Major department blocked, no workaround)
    "Users cannot access payroll portal",
    "Salesforce integration broken, sales team cannot log leads",
    "Customer checkout page is throwing 500 errors",
    "Finance team unable to export end-of-month billing report",

    # Medium Impact (Disrupted workflow, localized, or has workaround)
    "Shared office printer on 3rd floor is jammed",
    "Slow internet speeds reported in the main conference room",
    "External monitor not detecting laptop via docking station",
    "Cannot sync corporate calendar with mobile device",

    # Low Impact (Cosmetic, individual requests, non-urgent)
    "Minor UI issue in dashboard",
    "Typo found on the internal HR wiki page",
    "Requesting password reset for Adobe Creative Cloud",
    "Change default font style on company email signature template"
]

priority = [
    "medium", "critical", "critical", "critical",
    "high", "high", "high", "high",
    "medium", "medium", "medium", "medium",
    "low", "low", "low", "low"
]


# Initialize embedding model (Ollama with nomic-embed-text)
model = OllamaEmbeddings(model="nomic-embed-text")
ticket_embeddings = np.array([model.embed_query(t) for t in description])

# Initialize similarity retriever
retriever = NearestNeighbors(
    n_neighbors=3,
    metric="cosine"
)
retriever.fit(ticket_embeddings)

# Encode priority for classification
label_encoder = LabelEncoder()
encoded_priority = label_encoder.fit_transform(priority)

# Train XGBoost classifier
classifier = XGBClassifier()
classifier.fit(ticket_embeddings, encoded_priority)


def evaluate_model():
    X_train, X_test, y_train, y_test = train_test_split(
        ticket_embeddings, encoded_priority, test_size=0.2, random_state=42
    )

    eval_classifier = XGBClassifier()
    eval_classifier.fit(X_train, y_train)
    y_pred = eval_classifier.predict(X_test)

    print("=== MODEL EVALUATION ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred,
          target_names=label_encoder.classes_))


def run_single():
    new_ticket = "Remote workers unable to connect"
    print(f"Incoming: {new_ticket}\n")

    new_embeddings = np.array([model.embed_query(new_ticket)])
    distances, indices = retriever.kneighbors(new_embeddings)

    print("Similar description:")
    for idx in indices[0]:
        print(f"  - {description[idx]} -> {priority[idx]}")

    prediction = classifier.predict(new_embeddings)
    predicted_label = label_encoder.inverse_transform(prediction)
    print(f"\nPredicted impact: {predicted_label[0]}")


def run_batch():
    test_description = [
        "The entire cloud infrastructure is throwing a 502 Bad Gateway",
        "Marketing department cannot access the shared Google Drive",
        "Wi-Fi keeps dropping out in the cafeteria",
        "How do I request a new mechanical keyboard?",
    ]

    for new_ticket in test_description:
        print(f"\n[Incoming Ticket]: \"{new_ticket}\"")
        new_embeddings = np.array([model.embed_query(new_ticket)])
        distances, indices = retriever.kneighbors(new_embeddings)

        print("  Top 2 Similar Historical description:")
        for idx in indices[0][:2]:
            print(f"    - {description[idx]} -> ({priority[idx]})")

        prediction = classifier.predict(new_embeddings)
        predicted_label = label_encoder.inverse_transform(prediction)
        print(f"  Predicted Impact: {predicted_label[0].upper()}")


if __name__ == "__main__":
    # evaluate_model()
    run_single()
    # run_batch()
