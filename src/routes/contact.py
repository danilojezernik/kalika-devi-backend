"""
Routes Overview:
1. POST / - Endpoint for clients to send an email and store it in the database.
2. GET / - Retrieve all emails from the database (private route, requires authentication).
3. GET /{_id} - Retrieve an email by its ID (private route, requires authentication).
4. DELETE /{_id} - Delete an email by its ID (private route, requires authentication).
"""

from fastapi import APIRouter, Depends, HTTPException

from src.domain.contact import Contact
from src.services import db, emails
from src.services.security import get_current_user
from src.template import email_template

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


@router.post('/', operation_id='client_sent_email_public')
async def client_sent_email_public(emailing: Contact):
    """
    Route for sending an email and storing it in the database.

    Args:
        emailing (Contact): The email content provided in the request body.

    Returns:
        dict: A message indicating the status of the email sending and storage.

    Raises:
        HTTPException: If email sending fails or if there's an issue with storing the email data.
    """

    # Generate the HTML body for the email using the provided data
    body = email_template.html(name=emailing.name, surname=emailing.surname, email=emailing.email,
                               message=emailing.message)

    # Attempt to send the email using the emails module
    if not emails.send_email(email_from=emailing.email, subject='Dobil si email danilojezernik.com', body=body):
        # If sending fails, raise an HTTPException with a 500 status code and a detail message
        return HTTPException(status_code=500, detail='Email not sent')

    # Store email data in the database
    email_data = {
        "_id": emailing.id,
        "name": emailing.name,
        "surname": emailing.surname,
        "email": emailing.email,
        "message": emailing.message,
        "datum_vnosa": emailing.datum_vnosa
    }
    # Insert the email data into the 'contact' collection of the 'process' database
    db.process.contact.insert_one(email_data)

    # If the email is sent successfully and stored in the database, return a success message
    return {"message": "Message was sent"}


"""
THIS ROUTES ARE PRIVATE
"""


# Get all emails private
@router.get('/', operation_id='get_all_emails_private')
async def get_all_emails_private(current_user: str = Depends(get_current_user)):
    """
    This route handles the retrieval of all the projects from the database

    :return: a list of Projects objects containing all the projects in the database
    """

    # Retrieve all projects from the database using the find method
    cursor = db.process.contact.find()

    # Create a list of Projects objects by unpacking data from each document retrieved
    contact_list = [Contact(**document) for document in cursor]

    # Return the list of Blog objects
    return contact_list


@router.get('/{_id}', operation_id='get_email_by_id_admin')
async def get_email_by_id_admin(_id: str):
    """
    This route handles the retrieval of one email by its ID from the database

    :param _id: The ID of the contact to be retrieved
    :return: If the project is found, returns the contact data; otherwise, returns a 404 error
    """

    # Attempt to find a project in the database based on the provided ID
    cursor = db.process.contact.find_one({'_id': _id})

    # If no contact is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Contact by ID: ({_id}) not found!')
    else:

        # If the contact is found, convert the cursor data into a Contact object and return it
        return Contact(**cursor)


# Delete email by ID
@router.delete('/{_id}', operation_id='delete_email_by_id_private')
async def delete_email_by_id_private(_id: str, current_user: str = Depends(get_current_user)):
    """
    Route for deleting an email by its unique ID.

    Returns:
        dict: A message indicating the success or failure of the email deletion.

    Raises:
        HTTPException: If the email with the specified ID is not found (404 status code).
        :param _id: The unique ID of the email to be deleted
        :param current_user: Authenticated user
    """

    # Attempt to delete the email by its unique ID from the 'contact' collection of the 'process' database
    delete_result = db.process.contact.delete_one({'_id': _id})

    # Check if any email was deleted (deleted_count > 0)
    if delete_result.deleted_count > 0:
        # Return a success message if the email was deleted successfully
        return {'message': 'Email deleted successfully'}
    else:
        # If no email is found with the specified ID, raise an HTTPException with a 404 status code and a detail message
        raise HTTPException(status_code=404, detail=f'Email by ID: ({_id}) not found!')
