"""
Routes Overview:
1. GET / - Retrieve all newsletters from the database.
2. GET /{_id} - Retrieve a specific newsletter by its ID from the database.
3. DELETE /{_id} - Delete a specific newsletter by its ID from the database.
4. POST / - Add and send a new newsletter to all recipients.
"""

from fastapi import APIRouter, HTTPException, Depends

from src.domain.newsletter import Newsletter
from src.services import newsletters, db
from src.services.security import get_current_user
from src.template import newsletter_body

router = APIRouter()


# GET ALL NEWSLETTER
@router.get("/", operation_id="get_all_newsletter")
async def get_all_newsletter(current_user: str = Depends(get_current_user)) -> list[Newsletter]:
    """
    This route handles the retrieval of all newsletter from the database.

    Behavior:
    - Retrieves all newsletter from the database.
    - Returns a list of Newsletter objects.
    """

    cursor = db.process.newsletter.find()
    return [Newsletter(**document) for document in cursor]


# GET NEWSLETTER BY ID
@router.get('/{_id}', operation_id='get_newsletter_by_id')
async def get_newsletter_by_id(_id: str, current_user: str = Depends(get_current_user)):
    """
    This route handles the retrieval of a newsletter by its ID from the database.

    Parameters:
    - _id (str): ID of the newsletter to retrieve.

    Behavior:
    - Retrieves a newsletter by its ID from the database.
    - Returns the Newsletter object if found, or raises an exception if not found.
    """

    cursor = db.process.newsletter.find_one({'_id': _id})
    if cursor is None:
        raise HTTPException(status_code=400, detail=f'Newsletter by ID {_id} does not exist')
    else:
        return Newsletter(**cursor)


# DELETE NEWSLETTER BY ID
@router.delete('/{_id}', operation_id='delete_newsletter_by_id')
async def delete_newsletter_by_id(_id: str, current_user: str = Depends(get_current_user)):
    """
    Route to delete a newsletter by its ID from the database.

    Arguments:
        _id (str): The ID of the newsletter to be deleted.
        current_user: Locking parameter

    Returns:
        dict: A message indicating the status of the deletion.

    Raises:
        HTTPException: If the newsletter is not found for deletion.
    """

    # Attempt to delete the newsletter from the database
    delete_result = db.process.newsletter.delete_one({'_id': _id})

    # Check if the blog was successfully deleted
    if delete_result.deleted_count > 0:
        return {"message": "Newsletter was successfully deleted"}
    else:
        # Raise an exception if the newsletter was not found for deletion
        return HTTPException(status_code=404, detail=f'Newsletter by ID {_id} not found')


# SEND NEWSLETTER TO ALL
@router.post("/", operation_id="send_newsletter_to_all")
async def send_newsletter_to_all(newsletter: Newsletter, current_user: str = Depends(get_current_user)):
    """
    Route for sending a newsletter to all recipients.

    Parameters:
    - newsletter (Newsletter): The newsletter object containing title and content.

    Behavior:
    - Adds the newsletter to the database.
    - Generates HTML content for the newsletter.
    - Sends the newsletter as an email.
    - If successful, returns the newly created newsletter.
    - If any step fails, appropriate error responses are returned.
    """

    # Add a new newsletter to the database
    newsletter_dict = newsletter.dict(by_alias=True)
    insert_result = db.process.newsletter.insert_one(newsletter_dict)

    # Generate the HTML content for the newsletter
    body = newsletter_body.html_newsletter(title=newsletter.title, content=newsletter.content)

    # Send the newsletter to all
    if not newsletters.newsletter(subject='DaniloJezernik.com | E-novice ♥', body=body):
        # If sending the email fails, return a 500 Internal Server Error
        return HTTPException(status_code=500, detail="Email not sent")

    # Check if the insertion was acknowledged and update the blog's ID
    if insert_result.acknowledged:
        newsletter_dict['_id'] = str(insert_result.inserted_id)
        # Return the newly created newsletter
        return Newsletter(**newsletter_dict)
    else:
        # If the insertion was not acknowledged, return None
        return None
