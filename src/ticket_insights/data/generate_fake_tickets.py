import random
import csv
from datetime import datetime, timedelta
from typing import Any

from faker import Faker

from ticket_insights.aws.s3_client import upload_to_s3

fake = Faker()
Faker.seed(42)
random.seed(42)

subjects = [
    "Can't log in", "App keeps crashing", "Payment issue", "Feature request",
    "Data not syncing", "Account locked", "Error 500", "Password reset not working"
]

products = ["CoolApp", "TrackMate", "DataCloud", "Formify"]

statuses = ["Open", "Closed"]


def generate_ticket(ticket_id: int) -> dict[str, Any]:
    """
    Generate a fake support ticket record with random attributes.

    Args:
        ticket_id: Integer ID for the ticket.

    Returns:
        A dictionary representing the ticket with keys:
        'ticket_id', 'created_at', 'subject', 'description', 'status', 'product'.
    """
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


def generate_csv(file_path: str, count: int = 100) -> None:
    """
    Generate a CSV file of fake tickets and save it to the given path.

    Args:
        file_path: Path to output CSV file.
        count: Number of tickets to generate (default is 100).
    """
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["ticket_id", "created_at", "subject", "description", "status", "product"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for ticket_id in range(1, count + 1):
            writer.writerow(generate_ticket(ticket_id))


if __name__ == "__main__":
    generate_csv("ticket_insights/data/tickets.csv", count=100)
    upload_to_s3("ticket_insights/data/tickets.csv", "tickets.csv")
