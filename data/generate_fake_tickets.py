import random
import csv
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)

subjects = [
    "Can't log in", "App keeps crashing", "Payment issue", "Feature request",
    "Data not syncing", "Account locked", "Error 500", "Password reset not working"
]

products = ["CoolApp", "TrackMate", "DataCloud", "Formify"]

statuses = ["Open", "Closed"]

def generate_ticket(ticket_id):
    subject = random.choice(subjects)
    description = fake.paragraph(nb_sentences=3)
    created_at = fake.date_time_between(datetime(2025, 1, 1), datetime(2025, 4, 15))
    status = random.choices(statuses, weights=[0.4, 0.6])[0]
    product = random.choice(products)

    return {
        "ticket_id": ticket_id,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "subject": subject,
        "description": description,
        "status": status,
        "product": product
    }

def generate_csv(file_path, count=100):
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["ticket_id", "created_at", "subject", "description", "status", "product"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for ticket_id in range(1, count + 1):
            writer.writerow(generate_ticket(ticket_id))

if __name__ == "__main__":
    generate_csv("data/tickets.csv", count=100)
