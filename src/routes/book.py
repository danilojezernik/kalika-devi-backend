"""
Routes Overview:
1. GET / - Retrieve all books from the database.
2. GET /{_id} - Retrieve a book by its ID.
3. POST / - Add a new book to the database.
4. PUT /{_id} - Edit an existing book by its ID.
5. DELETE /{_id} - Delete a book by its ID.
"""

from fastapi import APIRouter, Depends, HTTPException

from src.domain.book import Book
from src.services import db

from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# Get all the book from database
@router.get('/', operation_id='get_all_book_public')
async def get_all_book_public() -> list[Book]:
    """
    This route handles the retrieval of all the book from the database

    :return: a list of Book objects containing all the book in the database
    """

    # Retrieve all blogs from the database using the find method
    cursor = db.process.book.find()

    # Create a list of Blog objects by unpacking data from each document retrieved
    book_list = [Book(**document) for document in cursor]

    # Return the list of Blog objects
    return book_list


# Get book by its ID
@router.get('/{_id}', operation_id='get_book_by_id_public')
async def get_book_by_id_public(_id: str):
    """
    This route handles the retrieval of one book by its ID from the database

    :param _id: The ID of the book to be retrieved
    :return: If the book is found, returns the book data; otherwise, returns a 404 error
    """

    # Attempt to find book in the database based on the provided ID
    cursor = db.process.book.find_one({'_id': _id})

    # If no book is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Book by ID: ({_id}) does not exist')
    else:
        # If the book is found, convert the cursor data into a Book object and return it
        return Book(**cursor)


"""
THIS ROUTES ARE PRIVATE
"""


# Get all the book from database
@router.get('/admin/', operation_id='get_all_book_private')
async def get_all_book_private(current_user: str = Depends(get_current_user)) -> list[Book]:
    """
    This route handles the retrieval of all the book from the database

    :return: a list of Book objects containing all the book in the database
    """

    # Retrieve all blogs from the database using the find method
    cursor = db.process.book.find()

    # Create a list of Blog objects by unpacking data from each document retrieved
    book_list = [Book(**document) for document in cursor]

    # Return the list of Blog objects
    return book_list


# Get book by its ID
@router.get('/admin/{_id}', operation_id='get_book_by_id_private')
async def get_book_by_id_private(_id: str, current_user: str = Depends(get_current_user)):
    """
    This route handles the retrieval of one book by its ID from the database

    :param current_user: Current user that is registered
    :param _id: The ID of the book to be retrieved
    :return: If the book is found, returns the book data; otherwise, returns a 404 error
    """

    # Attempt to find book in the database based on the provided ID
    cursor = db.process.book.find_one({'_id': _id})

    # If no book is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Book by ID: ({_id}) does not exist')
    else:
        # If the book is found, convert the cursor data into a Book object and return it
        return Book(**cursor)


# This route adds a new book
@router.post('/', operation_id='add_new_book_private')
async def add_new_book_private(book: Book,
                                      current_user: str = Depends(get_current_user)) -> Book | None:
    """
    Handles the addition of a new book to the database.

    :param book: The Book object representing the new book to be added.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the addition is successful, returns the newly added Book object; otherwise, returns None.
    """

    # Convert the Book object to a dictionary
    book_dict = book.dict(by_alias=True)

    # Insert book data into database
    insert_result = db.process.book.insert_one(book_dict)

    # Check if the insertion was acknowledged by the database
    if insert_result.acknowledged:

        # Update the dictionary with the newly assigned _id
        book_dict['_id'] = str(book_dict['_id'])

        # Return the newly added Book object
        return Book(**book_dict)
    else:

        # If the insertion was not acknowledged, return None
        return None


# Edit book by its ID
@router.put('/{_id}', operation_id='edit_book_by_id_private')
async def edit_book_by_id_private(_id: str, book: Book,
                                         current_user: str = Depends(get_current_user)):
    """
    Handles the editing of book by its ID in the database.

    :param _id: The ID of the book to be edited.
    :param book: The updated Book object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the book are successfully edited, returns the updated Book object; otherwise, returns None.
    """

    # Convert the Book object to a dictionary
    book_dict = book.dict(by_alias=True)

    # Delete the '_id' field from the book dictionary to avoid updating the ID
    del book_dict['_id']

    # Update the book in the database using the update_one method
    cursor = db.process.book.update_one({'_id': _id}, {'$set': book_dict})

    # Check if the book were successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated book from the database
        updated_document = db.process.book.find_one({'_id': _id})

        # Check if the updated book exist
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Book(**updated_document)

    # Return None if the book were not updated
    return None


# Delete book by ID
@router.delete("/{_id}", operation_id='delete_book_by_id_private')
async def delete_book_by_id_private(_id: str, current_user: str = Depends(get_current_user)):
    """
    Handles the deletion of book by its ID from the database.

    :param _id: The ID of the book to be deleted.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the book are successfully deleted, returns a success message; otherwise, raises a 404 error.
    """

    # Attempt to delete the book from the database using the delete_one method
    delete_results = db.process.book.delete_one({'_id': _id})

    # Check if the book were successfully deleted
    if delete_results.deleted_count > 0:
        # Return a success message if the book were found and deleted
        return {'message': 'Experience deleted successfully'}
    else:
        # If the book were not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f'Book with ID: ({_id}) not found!')
