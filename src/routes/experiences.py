"""
Routes Overview:
1. GET / - Retrieves all experiences from the database (public).
2. GET /{_id} - Retrieves a specific experience by its ID (public).
3. GET /admin/ - Retrieves all experiences from the database (private).
4. POST / - Adds a new experience to the database (private).
5. GET /admin/{_id} - Retrieves a specific experience by its ID (private).
6. PUT /{_id} - Updates an existing experience by its ID (private).
7. DELETE /{_id} - Deletes an experience from the database by its ID (private).
"""

from fastapi import APIRouter, Depends, HTTPException

from src.domain.experiences import Experiences
from src.services import db

from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all the experiences from database
@router.get('/', operation_id='get_all_experiences_public')
async def get_all_experiences_public() -> list[Experiences]:
    """
    This route handles the retrieval of all the experiences from the database

    :return: a list of Experiences objects containing all the experiences in the database
    """

    # Retrieve all blogs from the database using the find method
    cursor = db.process.experiences.find()

    # Create a list of Blog objects by unpacking data from each document retrieved
    experiences_list = [Experiences(**document) for document in cursor]

    # Return the list of Blog objects
    return experiences_list


# Get experiences by its ID
@router.get('/{_id}', operation_id='get_experiences_by_id_public')
async def get_experiences_by_id_public(_id: str):
    """
    This route handles the retrieval of one experiences by its ID from the database

    :param _id: The ID of the experiences to be retrieved
    :return: If the experiences is found, returns the experiences data; otherwise, returns a 404 error
    """

    # Attempt to find experiences in the database based on the provided ID
    cursor = db.process.experiences.find_one({'_id': _id})

    # If no experiences is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Experiences by ID: ({_id}) does not exist')
    else:
        # If the experiences is found, convert the cursor data into a Experiences object and return it
        return Experiences(**cursor)


"""
THIS ROUTES ARE PRIVATE
"""


# Get all the experiences from database
@router.get('/admin/', operation_id='get_all_experiences_private')
async def get_all_experiences_private(current_user: str = Depends(get_current_user)) -> list[Experiences]:
    """
    This route handles the retrieval of all the experiences from the database

    :return: a list of Experiences objects containing all the experiences in the database
    """

    # Retrieve all blogs from the database using the find method
    cursor = db.process.experiences.find()

    # Create a list of Blog objects by unpacking data from each document retrieved
    experiences_list = [Experiences(**document) for document in cursor]

    # Return the list of Blog objects
    return experiences_list


# Get experiences by its ID
@router.get('/admin/{_id}', operation_id='get_experiences_by_id_private')
async def get_experiences_by_id_private(_id: str, current_user: str = Depends(get_current_user)):
    """
    This route handles the retrieval of one experiences by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the experiences to be retrieved
    :return: If the experiences is found, returns the experiences data; otherwise, returns a 404 error
    """

    # Attempt to find experiences in the database based on the provided ID
    cursor = db.process.experiences.find_one({'_id': _id})

    # If no experiences is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Experiences by ID: ({_id}) does not exist')
    else:
        # If the experiences is found, convert the cursor data into a Experiences object and return it
        return Experiences(**cursor)


# This route adds a new experiences
@router.post('/', operation_id='add_new_experiences_private')
async def add_new_experiences_private(experiences: Experiences,
                                      current_user: str = Depends(get_current_user)) -> Experiences | None:
    """
    Handles the addition of a new experiences to the database.

    :param experiences: The Experiences object representing the new experiences to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added Experiences object; otherwise, returns None.
    """

    # Convert the Experiences object to a dictionary
    experiences_dict = experiences.dict(by_alias=True)

    # Insert experiences data into database
    insert_result = db.process.experiences.insert_one(experiences_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:

        # Update the dictionary with the newly assigned _id
        experiences_dict['_id'] = str(experiences_dict['_id'])

        # Return the newly added Experiences object
        return Experiences(**experiences_dict)
    else:

        # If the insertion was not acknowledged, return None
        return None


# Edit experiences by its ID
@router.put('/{_id}', operation_id='edit_experiences_by_id_private')
async def edit_experiences_by_id_private(_id: str, experiences: Experiences,
                                         current_user: str = Depends(get_current_user)):
    """
    Handles the editing of experiences by its ID in the database.

    :param _id: The ID of the experiences to be edited.
    :param experiences: The updated Experiences object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the experiences are successfully edited, returns the updated Experiences object; otherwise, returns None.
    """

    # Convert the Experiences object to a dictionary
    experiences_dict = experiences.dict(by_alias=True)

    # Delete the '_id' field from the experiences dictionary to avoid updating the ID
    del experiences_dict['_id']

    # Update the experiences in the database using the update_one method
    cursor = db.process.experiences.update_one({'_id': _id}, {'$set': experiences_dict})

    # Check if the experiences were successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated experiences from the database
        updated_document = db.process.experiences.find_one({'_id': _id})

        # Check if the updated experiences exist
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Experiences(**updated_document)

    # Return None if the experiences were not updated
    return None


# Delete experiences by ID
@router.delete("/{_id}", operation_id='delete_experiences_by_id_private')
async def delete_experiences_by_id_private(_id: str, current_user: str = Depends(get_current_user)):
    """
    Handles the deletion of experiences by its ID from the database.

    :param _id: The ID of the experiences to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the experiences are successfully deleted, returns a success message; otherwise, raises a 404 error.
    """

    # Attempt to delete the experiences from the database using the delete_one method
    delete_results = db.process.experiences.delete_one({'_id': _id})

    # Check if the experiences were successfully deleted
    if delete_results.deleted_count > 0:
        # Return a success message if the experiences were found and deleted
        return {'message': 'Experience deleted successfully'}
    else:
        # If the experiences were not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'Experiences with ID: ({_id}) not found!')
