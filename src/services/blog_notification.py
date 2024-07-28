from src.services.emails import fetch_email_addresses, send_emails


def blog_notification(subject: str, body: str) -> bool:
    """
    Sends a blog notification email to users who have opted in for blog notifications.

    Args:
        subject (str): The subject of the blog notification email.
        body (str): The HTML content of the blog notification email.

    Returns:
        bool: True if the email was sent successfully to all recipients, False otherwise.
    """

    # Fetch email addresses of users who have opted in for blog notifications
    email_addresses = fetch_email_addresses({'blog_notification': True})

    # Send the email to the fetched email addresses
    return send_emails(subject, body, email_addresses)
