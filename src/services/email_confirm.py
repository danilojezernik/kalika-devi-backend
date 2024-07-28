from email.message import EmailMessage
import smtplib

from src import env


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

    # TODO: ALENU NASTAVI GOOGLE PASSWORD ZA DOBIVANJE EMAILOV - PASSWORD + SENDER
    # Establish an SSL connection to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(env.EMAIL, env.PASSWORD)

        # Send the email from 'env.EMAIL_ME' to 'email_from'
        sendemail = smtp.sendmail(env.EMAIL, email_to, em.as_string())

        if not sendemail:
            return True  # Email sent successfully
        else:
            return False  # Failed to send the email
