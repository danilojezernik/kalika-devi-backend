"""
Routes Overview:
1. GET / - Retrieve all subscribers from the database.
2. GET /{_id} - Retrieve a subscriber by their ID.
3. POST / - Add a new subscriber to the database.
4. PUT /{_id} - Edit an existing subscriber by their ID.
5. DELETE /{_id} - Delete a subscriber by their ID.
6. POST /subscribe - Subscribe a client to the newsletter and send a confirmation email.
7. GET /confirm/{token} - Confirm a client's email for the newsletter subscription.
"""

from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse

from src import env
from src.domain.subscriber import Subscriber
from src.services import db, security, emails
from src.services.security import get_current_user
from src.template import confirmation_newsletter_email

router = APIRouter()


# GET ALL SUBSCRIBERS
@router.get("/", operation_id="get_all_subscribers")
async def get_all_subscribers(current_user: str = Depends(get_current_user)) -> list[Subscriber]:
    """
    This route handles the retrieval of all subscribers from the database.

    Behavior:
    - Retrieves all subscribers from the database.
    - Returns a list of Subscriber objects.
    """

    cursor = db.process.subscriber.find()
    return [Subscriber(**document) for document in cursor]


# GET SUBSCRIBER BY ID
@router.get("/{_id}", operation_id="get_subscriber_by_id")
async def get_subscriber_id(_id: str, current_user: str = Depends(get_current_user)):
    """
    This route handles the retrieval of a subscriber by its ID from the database.

    Parameters:
    - _id (str): ID of the subscriber to retrieve.

    Behavior:
    - Retrieves a subscriber by its ID from the database.
    - Returns the Subscriber object if found, or raises an exception if not found.
    """

    # Retrieve a blog by its ID from the database
    cursor = db.process.subscriber.find_one({'_id': _id})
    if cursor is None:
        raise HTTPException(status_code=400, detail=f"Subscriber by ID:{_id} does not exist")
    else:
        return Subscriber(**cursor)


# ADD SUBSCRIBER
@router.post("/", operation_id="add_subscriber")
async def post_subscriber(subscriber: Subscriber, current_user: str = Depends(get_current_user)) -> Subscriber | None:
    """
    This route adds a new subscriber to the database.

    Parameters:
    - subscriber (Subscriber): The subscriber object to be added.
    - current_user (str): The username of the authenticated user.

    Behavior:
    - Adds a new subscriber to the database.
    - Returns the added Subscriber object if successful, or None if unsuccessful.
    """

    # Add a new blog to the database
    subscriber_dict = subscriber.dict(by_alias=True)
    insert_result = db.process.subscriber.insert_one(subscriber_dict)

    # Check if the insertion was acknowledged and update the blog's ID
    if insert_result.acknowledged:
        subscriber_dict['_id'] = str(insert_result.inserted_id)
        return Subscriber(**subscriber_dict)
    else:
        return None


# EDIT SUBSCRIBER BY ID
@router.put("/{_id}")
async def edit_subscriber(_id: str, subscriber: Subscriber,
                          current_user: str = Depends(get_current_user)) -> Subscriber | None:
    """
    This route edits an existing subscriber by its ID in the database.

    Parameters:
    - _id (str): The ID of the subscriber to be edited.
    - blog (Blog): The updated subscriber object.
    - current_user (str): The username of the authenticated user.

    Behavior:
    - Edits an existing subscriber by its ID in the database.
    - Returns the updated Subscriber object if successful, or None if unsuccessful.
    """

    # Edit an existing subscriber by its ID in the database
    subscriber = subscriber.dict(by_alias=True)
    del subscriber['_id']

    # Update the newsletter in the database
    cursor = db.process.subscriber.update_one({'_id': _id}, {'$set': subscriber})

    # Check if the newsletter was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated newsletter from the database
        updated_document = db.process.subscriber.find_one({'_id': _id})

        # Check if the updated newsletter exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Subscriber(**updated_document)

    # Return None if the newsletter was not updated
    return None


# DELETE SUBSCRIBER BY ID
@router.delete("/{_id}", operation_id="delete_subscriber")
async def delete_subscriber(_id: str, current_user: str = Depends(get_current_user)):
    """
    Route to delete a blog by its ID from the database.

    Arguments:
        _id (str): The ID of the blog to be deleted.
        current_user (str): The current authenticated user.

    Returns:
        dict: A message indicating the status of the deletion.

    Raises:
        HTTPException: If the blog is not found for deletion.
    """

    # Attempt to delete the blog from the database
    delete_result = db.process.subscriber.delete_one({'_id': _id})

    # Check if the blog was successfully deleted
    if delete_result.deleted_count > 0:
        return {"message": "Subscriber deleted successfully"}
    else:
        # Raise an exception if the blog was not found for deletion
        raise HTTPException(status_code=404, detail=f"Subscriber by ID:({_id}) not found")


# CLIENT SUBSCRIPTION TO NEWSLETTER
@router.post("/subscribe")
async def subscribe(subscriber: Subscriber):
    """
    Route for subscribing a client to the newsletter and sending a confirmation email.

    Parameters:
    - subscriber (Subscriber): Subscriber object containing client information.

    Behavior:
    - Creates an access token for the client with a short expiration time.
    - Sends a confirmation email to the client with a confirmation link.
    - Inserts the subscriber's data into the database.
    - Returns a success message if everything is successful.
    - If any step fails, returns an appropriate error response.
    """

    # Create an access token with a short expiration time
    token = security.create_access_token(data={'user_id': subscriber.id}, expires_delta=timedelta(minutes=10))

    # Generate the confirmation email's HTML content
    body = confirmation_newsletter_email.html(link=f'{env.DOMAIN}/subscribers/confirm/{token}', name=subscriber.name,
                                              surname=subscriber.surname)

    # Send the confirmation email to the subscriber
    if not emails.send_confirm(email_to=subscriber.email,
                               subject='DaniloJezernik.com | Potrdite svojo registracijo na E-novičke ♥', body=body):
        return HTTPException(status_code=500, detail="Email not sent")

    # Insert the subscriber's data into the database
    db.process.subscriber.insert_one(subscriber.dict(by_alias=True))

    return {"message": "Message was sent"}


# CLIENT CONFIRMING EMAIL FOR NEWSLETTER
@router.get("/confirm/{token}")
async def confirm(token: str):
    """
    Route for clients to confirm their subscription by clicking on the confirmation link.

    Parameters:
    - token (str): The confirmation token.

    Behavior:
    - Extracts the user_id from the token.
    - Marks the subscriber as confirmed in the database.
    - Returns the payload from the token, which can be useful for additional actions.
    """

    # Extract the user_id from the confirmation token
    payload = await security.get_payload(token=token)

    # Mark the subscriber as confirmed in the database
    db.process.subscriber.update_one({"_id": payload['user_id']}, {"$set": {"confirmed": True}})

    return RedirectResponse(url=f'{env.DOMAIN}/index', status_code=status.HTTP_303_SEE_OTHER)
