"""
Routes Overview:
1. GET / - Retrieve all projects from the database.
2. GET /{_id} - Retrieve a specific project by its ID from the database.
3. DELETE /{_id} - Delete a specific project by its ID from the database.
4. POST / - Add a new project to the database.
5. PUT /{_id} - Edit an existing project by its ID in the database.
"""

from fastapi import APIRouter, Depends, HTTPException

from src.domain.projects import Projects
from src.services import db

from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all projects public
@router.get('/', operation_id='get_all_projects_public')
async def get_all_projects_public():
    """
    This route handles the retrieval of all the projects from the database

    :return: a list of Projects objects containing all the projects in the database
    """

    # Retrieve all projects from the database using the find method
    cursor = db.process.projects.find()

    # Create a list of Projects objects by unpacking data from each document retrieved
    projects_lists = [Projects(**document) for document in cursor]

    # Return the list of Blog objects
    return projects_lists


# Get project by ID
@router.get('/{_id}', operation_id='get_projects_by_id_public')
async def get_projects_by_id_public(_id: str) -> Projects:
    """
    This route handles the retrieval of one project by its ID from the database

    :param _id: The ID of the project to be retrieved
    :return: If the project is found, returns the project data; otherwise, returns a 404 error
    """

    # Attempt to find a project in the database based on the provided ID
    cursor = db.process.projects.find_one({'_id': _id})

    # If no project is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Project by ID: ({_id}) not found!')
    else:

        # If the project is found, convert the cursor data into a Projects object and return it
        return Projects(**cursor)


"""
THIS ROUTES ARE PRIVATE
"""


# Get all projects private
@router.get('/admin/', operation_id='get_all_projects_private')
async def get_all_projects_private(current_user: str = Depends(get_current_user)):
    """
    This route handles the retrieval of all the blogs from the database

    :return: a list of Blog objects containing all the blogs in the database
    """

    # Retrieve all projects from the database using the find method
    cursor = db.process.projects.find()

    # Create a list of Projects objects by unpacking data from each document retrieved
    projects_lists = [Projects(**document) for document in cursor]

    # Return the list of Blog objects
    return projects_lists


# Get project by ID
@router.get('/admin/{_id}', operation_id='get_projects_by_id_private')
async def get_projects_by_id_private(_id: str, current_user: str = Depends(get_current_user)):
    """
    This route handles the retrieval of one project by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the project to be retrieved
    :return: If the project is found, returns the project data; otherwise, returns a 404 error
    """

    # Attempt to find a project in the database based on the provided ID
    cursor = db.process.projects.find_one({'_id': _id})

    # If no project is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Project by ID: ({_id}) not found!')
    else:

        # If the project is found, convert the cursor data into a Projects object and return it
        return Projects(**cursor)


# Add new project
@router.post('/', operation_id='add_new_project_private')
async def add_new_project_private(project: Projects, current_user: str = Depends(get_current_user)) -> Projects | None:
    """
    Handles the addition of a new project to the database.

    :param project: The Projects object representing the new project to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added Projects object; otherwise, returns None.
    """

    # Convert the Projects object to a dictionary
    project_dict = project.dict(by_alias=True)

    # Insert the project data into the database
    insert_result = db.process.projects.insert_one(project_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:

        # Update the dictionary with the newly assigned _id
        project_dict['_id'] = str(insert_result.inserted_id)

        # Return the newly added Projects object
        return Projects(**project_dict)
    else:

        # If the insertion was not acknowledged, return None
        return None


# Edit project by ID
@router.put('/{_id}', operation_id='edit_project_by_id_private')
async def edit_project_by_id_private(_id: str, project: Projects,
                                     current_user: str = Depends(get_current_user)) -> Projects | None:
    """
    Handles the editing of a project by its ID in the database.

    :param _id: The ID of the project to be edited.
    :param project: The updated Projects object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the project is successfully edited, returns the updated Projects object; otherwise, returns None.
    """

    # Convert the Projects object to a dictionary
    project_dict = project.dict(by_alias=True)

    # Delete the '_id' field from the project dictionary to avoid updating the ID
    del project_dict['_id']

    # Update the project in the database using the update_one method
    cursor = db.process.projects.update_one({'_id': _id}, {'$set': project_dict})

    # Check if the project was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated project from the database
        updated_document = db.process.projects.find_one({'_id': _id})

        # Check if the updated project exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Projects(**updated_document)

    else:

        # Return None if the project was not updated
        return None


# Delete project by ID
@router.delete('/{_id}', operation_id='delete_project_by_id_private')
async def delete_project_by_id_private(_id: str):
    delete_result = db.process.projects.delete_one({'_id': _id})

    if delete_result.deleted_count > 0:
        return {'message': 'Project deleted successfully'}
    else:
        raise HTTPException(status_code=404, detail=f'Project by ID: ({_id}) not found!')
