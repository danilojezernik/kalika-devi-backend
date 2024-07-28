"""
Routes:
1. GET all technologies - Retrieve all technologies from the database.
2. GET technology by ID - Retrieve a specific technology by its ID.
3. GET limited technologies - Retrieve a limited number of technologies.
4. GET all technologies (private) - Retrieve all technologies for authenticated users.
5. GET technology by ID (private) - Retrieve a specific technology by its ID for authenticated users.
6. ADD a new technology - Add a new technology to the database.
7. EDIT a technology by ID - Edit an existing technology by its ID.
8. DELETE a technology by ID - Delete a technology by its ID.
"""

from fastapi import APIRouter, Depends, HTTPException

from src.domain.technology import Technology
from src.services import db
from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# This route gets all the technologies from the database
@router.get('/', operation_id='get_all_technologies_public')
async def get_all_technologies_public() -> list[Technology]:
    """
    This route handles the retrieval of all the technologies from the database

    :return: a list of Technology objects containing all the technologies in the database
    """

    # Retrieve all technologies from the database using the find method
    cursor = db.process.technology.find()

    # Create a list of Technology objects by unpacking data from each document retrieved
    technology_list = [Technology(**document) for document in cursor]

    # Return the list of Technology objects
    return technology_list


# This route get one technology by its ID
@router.get('/{_id}', operation_id='get_technology_by_id_public')
async def get_technology_by_id_public(_id: str):
    """
    This route handles the retrieval of one technology by its ID from the database

    :param _id: The ID of the technology to be retrieved
    :return: If the technology is found, returns the technology data; otherwise, returns a 404 error
    """

    # Attempt to find a technology in the database based on the provided ID
    cursor = db.process.technology.find_one({'_id': _id})

    # If no technology is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Technology by ID: ({_id}) does not exist')
    else:

        # If the technology is found, convert the cursor data into a Technology object and return it
        return Technology(**cursor)


# This route gets a limited amount of technologies
@router.get('/limited/', operation_id='get_limited_technologies')
async def get_limited_technologies(limit: int = 4) -> list[Technology]:
    """
    Handles the retrieval of a limited amount of technologies from the database.

    :param limit: The maximum number of technologies to retrieve (default is 2).
    :return: A list of Technology objects containing information about the limited technologies.
    """

    # Retrieve a limited number of technologies from the database using the limit method
    cursor = db.process.technology.find().limit(limit)

    # Create a list of Technology objects by unpacking data from each document retrieved
    technology_limited_list = [Technology(**document) for document in cursor]

    # Return the list of Technology objects
    return technology_limited_list


"""
THIS ROUTES ARE PRIVATE

User/Admin has to login!
"""


# This route gets all the technologies from the database
@router.get('/admin/', operation_id='get_all_technologies_private')
async def get_all_technologies_private(current_user: str = Depends(get_current_user)) -> list[Technology]:
    """
    This route handles the retrieval of all the technologies from the database

    :return: a list of Technology objects
    """

    # Retrieve all technologies from the database using the find method
    cursor = db.process.technology.find()

    # Create a list of Technology objects by unpacking data from each document retrieved
    technology_list = [Technology(**document) for document in cursor]

    # Return the list of Technology objects
    return technology_list


# This route get one technology by its ID
@router.get('/admin/{_id}', operation_id='get_technology_by_id_private')
async def get_technology_by_id_private(_id: str, current_user: str = Depends(get_current_user)) -> Technology:
    """
    This route handles the retrieval of one technology by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the technology to be retrieved
    :return: If the technology is found, returns the technology data; otherwise, returns a 404 error
    """

    # Attempt to find a technology in the database based on the provided ID
    cursor = db.process.technology.find_one({'_id': _id})

    # If no technology is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Technology by ID: ({_id}) does not exist')
    else:
        # If the technology is found, convert the cursor data into a Technology object and return it
        return Technology(**cursor)


# This route adds a new technology
@router.post('/', operation_id='add_new_technology_private')
async def add_new_technology(technology: Technology, current_user: str = Depends(get_current_user)) -> Technology | None:
    """
    Handles the addition of a new technology to the database.

    :param technology: The Technology object representing the new technology to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added Technology object; otherwise, returns None.
    """

    # Convert the Technology object to a dictionary for database insertion
    technology_dict = technology.dict(by_alias=True)

    # Insert the technology data into the database
    insert_result = db.process.technology.insert_one(technology_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:
        # If insertion is successful, update the dictionary with the newly assigned _id
        technology_dict['_id'] = str(insert_result.inserted_id)

        # Return the newly added Technology object, using the updated dictionary
        return Technology(**technology_dict)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# This route is to edit a technology by its ID
@router.put('/{_id}', operation_id='edit_technology_by_id_private')
async def edit_technology_by_id_private(_id: str, technology: Technology, current_user: str = Depends(get_current_user)) -> Technology | None:
    """
    Handles the editing of a technology by its ID in the database.

    :param _id: The ID of the technology to be edited.
    :param technology: The updated Technology object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the technology is successfully edited, returns the updated Technology object; otherwise, returns None.
    """

    # Convert the Technology object to a dictionary
    technology_dict = technology.dict(by_alias=True)
    print(technology_dict)
    # Delete the '_id' field from the technology dictionary to avoid updating the ID
    del technology_dict['_id']

    # Update the technology in the database using the update_one method
    cursor = db.process.technology.update_one({'_id': _id}, {'$set': technology_dict})

    print(cursor)
    # Check if the technology was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated technology from the database
        updated_document = db.process.technology.find_one({'_id': _id})

        # Check if the updated technology exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Technology(**updated_document)

    # Return None if the technology was not updated
    return None


# Delete a technology by its ID from the database
@router.delete('/{_id}', operation_id='delete_technology_by_id_private')
async def delete_technology_by_id_private(_id: str, current_user: str = Depends(get_current_user)):
    """
    Handles the deletion of a technology by its ID from the database.

    :param _id: The ID of the technology to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the technology is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the technology from the database using the delete_one method
    delete_result = db.process.technology.delete_one({'_id': _id})

    # Check if the technology was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'Technology deleted successfully!'}
    else:
        # If the technology was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'Technology by ID: ({_id}) not found!')
