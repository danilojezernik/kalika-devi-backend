"""
Routes Overview:
1. GET / - Retrieve all links from the database.
2. GET /admin/ - Retrieve all links from the database (private).
3. POST / - Add a new link to the database (private).
4. GET /{_id} - Retrieve a link by its ID (private).
5. PUT /{_id} - Edit a link by its ID (private).
6. DELETE /{_id} - Delete a link by its ID (private).
"""

from fastapi import APIRouter, Depends, HTTPException

from src.domain.links import Links
from src.services import db

from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all the links from database
@router.get('/', operation_id='get_all_links_public')
async def get_all_links_public() -> list[Links]:
    """
    This route handles the retrieval of all the links from the database

    :return: a list of Links objects containing all the links in the database
    """

    # Retrieve all links from the database using the find method
    cursor = db.process.links.find()

    # Create a list of Links objects by unpacking data from each document retrieved
    links_list = [Links(**document) for document in cursor]

    # Return the list of Links objects
    return links_list


# Get link by ID
@router.get('/{_id}', operation_id='get_link_by_id')
async def get_link_by_id(_id: str) -> Links:
    """
    This route handles the retrieval of one link by its ID from the database

    :param _id: The ID of the link to be retrieved
    :return: If the link is found, returns the link data; otherwise, returns a 404 error
    """

    # Attempt to find a link in the database based on the provided ID
    cursor = db.process.links.find_one({'_id': _id})

    # If no user is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Link by ID: ({_id}) does not exist')
    else:
        # If the link is found, convert the cursor data into a Links object and return it
        return Links(**cursor)


"""
THIS ROUTES ARE PRIVATE
"""


# Get all the links from database
@router.get('/admin/', operation_id='get_all_links_private')
async def get_all_links_private(current_user: str = Depends(get_current_user)) -> list[Links]:
    """
    This route handles the retrieval of all the links from the database

    :return: a list of Links objects containing all the links in the database
    """

    # Retrieve all links from the database using the find method
    cursor = db.process.links.find()

    # Create a list of Links objects by unpacking data from each document retrieved
    links_list = [Links(**document) for document in cursor]

    # Return the list of Links objects
    return links_list


# Add new link
@router.post('/', operation_id='add_new_link_private')
async def add_new_link_private(links: Links, current_user: str = Depends(get_current_user)) -> Links | None:
    """
    Handles the addition of a new links to the database.

    :param links: The Links object representing the new links to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added Links object; otherwise, returns None.
    """

    # Convert the Links object to a dictionary
    links_dict = links.dict(by_alias=True)

    # Insert the links data into the database
    insert_result = db.process.links.insert_one(links_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:

        # Update the dictionary with the newly assigned _id
        links_dict['_id'] = str(insert_result.inserted_id)

        # Return the newly added Links object
        return Links(**links_dict)

    else:

        # If the insertion was not acknowledged, return None
        return None


# Edit link by its ID
@router.put('/{_id}', operation_id='edit_link_private')
async def edit_link_private(_id: str, links: Links, current_user: str = Depends(get_current_user)) -> Links | None:
    """
    Handles the editing of a links by its ID in the database.

    :param _id: The ID of the links to be edited.
    :param links: The updated Links object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the links is successfully edited, returns the updated Links object; otherwise, returns None.
    """

    # Convert the Links object to a dictionary
    links_dict = links.dict(by_alias=True)

    # Delete the '_id' field from the links dictionary to avoid updating the ID
    del links_dict['_id']

    # Update the links in the database using the update_one method
    cursor = db.process.links.update_one({'_id': _id}, {'$set': links_dict})

    # Check if links was successfully updated
    if cursor.modified_count > 0:

        # Retrieve the updated links from the database
        updated_document = db.process.links.find_one({'_id': _id})

        # Check if the updated links exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Links(**updated_document)

    # Return None if the blog was not updated
    return None


# Delete link by its ID
@router.delete('/{_id}', operation_id='delete_links_by_id_private')
async def delete_links_by_id_private(_id: str, current_user: str = Depends(get_current_user)):
    """
    Handles the deletion of a link by its ID from the database.

    :param _id: The ID of the link to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the link is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the link from the database using the delete_one method
    delete_result = db.process.links.delete_one({'_id': _id})

    # Check if the link was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'Link deleted successfully'}
    else:

        # If the link was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'Link by ID: ({_id}) not found')
