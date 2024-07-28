"""
Routes Overview:
1. GET / - Retrieves all users from the database (public).
2. GET /{_id} - Retrieves a user by their ID (public).
3. GET /admin/ - Retrieves all users from the database (private).
4. POST / - Adds a new user to the database (private).
5. GET /admin/{_id} - Retrieves a user by their ID (private).
6. PUT /{_id} - Edits a user by their ID (private).
7. DELETE /{_id} - Deletes a user by their ID (private).
"""

from fastapi import APIRouter, Depends, HTTPException

from src.domain.user import User
from src.services import db
from src.services.security import get_current_user, pwd_context, make_hash

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all users from database
@router.get('/', operation_id='get_user_public')
async def get_user_public() -> list[User]:
    """
    This route handles the retrieval of all the users from the database

    :return: a list of Users objects containing all the users in the database
    """

    # Retrieve all users from the database using the find method
    cursor = db.process.user.find()

    # Create a list of Users objects by unpacking data from each document retrieved
    user_list = [User(**document) for document in cursor]

    # Return the list of User objects
    return user_list


# Get user by ID
@router.get('/{_id}', operation_id='get_user_by_id')
async def get_user_by_id(_id: str) -> User:
    """
    This route handles the retrieval of one user by its ID from the database

    :param _id: The ID of the user to be retrieved
    :return: If the user is found, returns the user data; otherwise, returns a 404 error
    """

    # Attempt to find a user in the database based on the provided ID
    cursor = db.process.user.find_one({'_id': _id})

    # If no user is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Blog by ID: ({_id}) does not exist')
    else:
        # If the user is found, convert the cursor data into a User object and return it
        return User(**cursor)


"""
THIS ROUTES ARE PRIVATE
"""


# Get all users from database
@router.get('/admin/', operation_id='get_user_private')
async def get_user_private(current_user: str = Depends(get_current_user)) -> list[User]:
    """
    This route handles the retrieval of all the users from the database

    :return: a list of Users objects containing all the users in the database
    """

    # Retrieve all users from the database using the find method
    cursor = db.process.user.find()

    # Create a list of Users objects by unpacking data from each document retrieved
    user_list = [User(**document) for document in cursor]

    # Return the list of User objects
    return user_list


# ADD USER BY ID
@router.post('/', operation_id='add_new_user')
async def add_new_user(user_data: User, current_user: str = Depends(get_current_user)) -> User | None:
    """
    This route adds a new user to the database.

    Parameters:
    - user_data (User): The user object containing user details to be added.

    Behavior:
    - Hashes the user's password.
    - Creates a new User object with the provided data.
    - Inserts the new user into the database.
    - Returns the added User object if successful, or None if unsuccessful.
    """

    print(user_data)

    # Hash the user's password for security
    hashed_password = make_hash(user_data.hashed_password)

    # Create a User object with the provided data, including the hashed password
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        description=user_data.description,
        profession=user_data.profession,
        technology=user_data.technology,
        disabled=False,  # Set the user as enabled by default
        confirmed=user_data.confirmed,
        registered=user_data.registered,
        blog_notification=user_data.blog_notification,
    ).dict(by_alias=True)

    print(new_user)
    # Insert the new user into the database
    insert_user = db.process.user.insert_one(new_user)

    # Check if the insertion was acknowledged by the database
    if insert_user.acknowledged:
        # If insertion is successful, update the dictionary with the newly assigned _id
        new_user['_id'] = str(insert_user.inserted_id)
        return User(**new_user)
    else:
        # If the insertion was not acknowledged, return None to indicate failure
        return None


# Get user by ID
@router.get('/admin/{_id}', operation_id='get_user_by_id_admin')
async def get_user_by_id_admin(_id: str, current_user: str = Depends(get_current_user)) -> User:
    """
    This route handles the retrieval of one user by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the user to be retrieved
    :return: If the user is found, returns the user data; otherwise, returns a 404 error
    """

    # Attempt to find a user in the database based on the provided ID
    cursor = db.process.user.find_one({'_id': _id})

    # If no user is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Blog by ID: ({_id}) does not exist')
    else:
        # If the user is found, convert the cursor data into a User object and return it
        return User(**cursor)


# Define a route for updating a user by ID - password is hashed when changed
@router.put('/{_id}', operation_id='edit_user_by_id')
async def edit_user_by_id(_id: str, user: User, current_user: str = Depends(get_current_user)) -> User | None:
    """
    Handles the editing of a user by its ID in the database.

    :param current_user: The current user, obtained from the authentication system.
    :param _id: The ID of the user to be edited.
    :param user: The updated User object with the new data.
    :return: If the user is successfully edited, returns the updated User object; otherwise, returns None.
    """

    # Convert the user object to a dictionary with alias
    user_dict = user.dict(by_alias=True)

    # Check if the user wants to update the password
    if 'hashed_password' in user_dict and user_dict['hashed_password']:
        # Hash the provided password using pwd_context.hash
        hashed_password = pwd_context.hash(user_dict['hashed_password'])
        user_dict['hashed_password'] = hashed_password
    else:
        # Remove the 'hashed_password' key if it exists but is empty
        user_dict.pop('hashed_password', None)

    # Remove '_id' from the dictionary as it shouldn't be updated
    user_dict.pop('_id', None)

    # Update the user document in the database
    cursor = db.process.user.update_one({'_id': _id}, {'$set': user_dict})

    # Check if the user was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated user from the database
        updated_document = db.process.user.find_one({'_id': _id})

        # Check if the updated user exists
        if updated_document:
            # Convert the ObjectId to a string for the User model
            updated_document['_id'] = str(updated_document['_id'])
            # Create a User instance from the updated document
            return User(**updated_document)

    # Return None if the user was not updated
    return None


# Delete user by ID
@router.delete('/{_id}', operation_id='delete_user_by_id')
async def delete_user_by_id(_id: str, current_user: str = Depends(get_current_user)):
    """
    Handles the deletion of a user by its ID from the database.

    :param _id: The ID of the user to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the user is successfully deleted, returns a message; otherwise, raises a 404 error.
    """

    # Attempt to delete the blog from the database using the delete_one method
    delete_result = db.process.user.delete_one({'_id': _id})

    # Check if the blog was successfully deleted
    if delete_result.deleted_count > 0:
        return {'message': 'User deleted successfully'}
    else:
        # If the blog was not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'User by ID: ({_id}) not found!')
