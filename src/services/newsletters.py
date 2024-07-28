from src.services.emails import fetch_email_addresses_newsletter, send_emails


def newsletter(subject: str, body: str) -> bool:
    """
    Sends a newsletter email to all subscribers.

    Args:
        subject (str): The subject of the newsletter email.
        body (str): The HTML content of the newsletter email.

    Returns:
        bool: True if the email was sent successfully to all subscribers, False otherwise.
    """

    # Fetch email addresses of all subscribers
    email_addresses = fetch_email_addresses_newsletter({})

    # Send the email to the fetched email addresses
    return send_emails(subject, body, email_addresses)
