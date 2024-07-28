import smtplib
from email.message import EmailMessage

from src import env
from src.services import db


def send_email(email_from: str, subject: str, body: str) -> bool:
    """
    Email a specified recipient.

    Args:
        email_from (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The HTML content of the email.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Note:
        This function sends an email to a specified recipient using the SMTP protocol to connect to Gmail's SMTP server.
        It's intended for sending individual emails. Before using this function, ensure that you have set up the Gmail
        sender email and password in the environment variables 'env.EMAIL_ME' and 'env.EMAIL_PASSWORD'. Additionally,
        the 'env.EMAIL_ME' should be set to the same Gmail account used for SMTP login.

    Dependencies:
        - Python's smtplib module for sending emails
    """

    # Create an EmailMessage object
    em = EmailMessage()
    em['From'] = email_from
    em['To'] = env.EMAIL
    em['Subject'] = subject
    em.set_content(body, subtype='html')

    # Establish an SSL connection to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(env.EMAIL, env.PASSWORD)

        # Send the email from 'env.EMAIL' to 'email_from'
        sendemail = smtp.sendmail(env.EMAIL, env.EMAIL, em.as_string())

        if not sendemail:
            return True
        else:
            return False


def send_confirm(email_to: str, subject: str, body: str) -> bool:
    """
    Send a confirmation email to a specified recipient.

    Args:
        email_to (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The HTML content of the email.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Note:
        This function sends an email to a specified recipient using the SMTP protocol to connect to Gmail's SMTP server.
        It's intended for sending individual emails. Before using this function, ensure that you have set up the Gmail
        sender email and password in the environment variables 'env.EMAIL_ME' and 'env.EMAIL_PASSWORD'. Additionally,
        the 'env.EMAIL_ME' should be set to the same Gmail account used for SMTP login.

    Dependencies:
        - Python's smtplib module for sending emails
    """

    # Create an EmailMessage object
    em = EmailMessage()
    em['From'] = env.EMAIL
    em['To'] = email_to
    em['Subject'] = subject
    em.set_content(body, subtype='html')

    # Establish an SSL connection to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(env.EMAIL, env.PASSWORD)

        # Send the email from 'env.EMAIL_ME' to 'email_from'
        sendemail = smtp.sendmail(env.EMAIL, email_to, em.as_string())

        if not sendemail:
            return True  # Email sent successfully
        else:
            return False  # Failed to send the email


def fetch_email_addresses(filter_criteria: dict) -> list:
    """
    Fetch email addresses from the database based on the provided filter criteria for new blog notification.

    Args:
        filter_criteria (dict): The filter criteria for querying the database.

    Returns:
        list: A list of email addresses that match the filter criteria for new blog notification.
    """
    cursor = db.process.user.find(filter_criteria, {'email': 1})
    email_addresses = [document['email'] for document in cursor]
    return email_addresses


def fetch_email_addresses_newsletter(filter_criteria: dict) -> list:
    """
    Fetch email addresses from the database based on the provided filter criteria for all subscribers.

    Args:
        filter_criteria (dict): The filter criteria for querying the database.

    Returns:
        list: A list of email addresses that match the filter criteria for subscribers.
    """
    cursor = db.process.subscriber.find(filter_criteria, {'email': 1})
    email_addresses = [document['email'] for document in cursor]
    return email_addresses


def send_emails(subject: str, body: str, email_addresses: list) -> bool:
    """
    Email a list of recipients.

    Args:
        subject (str): The subject of the email.
        body (str): The HTML content of the email.
        email_addresses (list): A list of email addresses to send the email to.

    Returns:
        bool: True if the email was sent successfully to all recipients, False otherwise.
    """
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(env.EMAIL, env.PASSWORD)

        for recipient in email_addresses:
            em = EmailMessage()
            em['From'] = env.EMAIL
            em['To'] = recipient
            em['Subject'] = subject
            em.set_content(body, subtype='html')

            try:
                smtp.send_message(em)
            except Exception as e:
                print(f"Failed to send email to {recipient}: {e}")
                return False

    return True


def newsletter(subject: str, body: str) -> bool:
    """
    Send a newsletter email to a list of subscribers.

    Args:
        subject (str): The subject of the newsletter email.
        body (str): The HTML content of the newsletter email.

    Returns:
        bool: True if the newsletter email was sent successfully to all subscribers, False otherwise.
    """
    try:
        # Retrieve email addresses of subscribers from the database
        cursor = db.process.subscriber.find({}, {'email': 1})
        email_addresses = [document['email'] for document in cursor]

        # Establish an SSL connection to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(env.EMAIL, env.EMAIL)

            for recipient in email_addresses:
                # Create an EmailMessage object for each recipient
                em = EmailMessage()
                em['From'] = env.EMAIL
                em['To'] = recipient
                em['Subject'] = subject
                em.set_content(body, subtype='html')

                # Send the email to the individual recipient
                smtp.send_message(em)

        return True  # Newsletter email sent successfully to all subscribers

    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        print(f"General error occurred: {e}")
        return False