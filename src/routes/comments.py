"""
Routes Overview:
1. GET / - Retrieve all comments from the database.
2. GET /{blog_id} - Retrieve all comments for a specific blog post from the database.
3. POST /{blog_id} - Add a new comment to a specific blog post in the database.
4. PUT /{blog_id}/{comment_id} - Edit an existing comment by its ID for a specific blog post.
5. DELETE /{blog_id}/{comment_id} - Delete a comment by its ID for a specific blog post.
"""

from fastapi import APIRouter

from src.domain.comments import Comment
from src.services import db

router = APIRouter()


# This route gets all comments from the database
@router.get("/", operation_id="get_all_comments")
async def get_comments_for_post() -> list[Comment]:
    """
    This route handles the retrieval of all comments from the database

    :return: a list of Comment objects containing all the comments in the database
    """

    # Retrieve all comments from the database using the find method
    cursor = db.process.comment.find()

    # Create a list of Comment objects by unpacking data from each document retrieved
    return [Comment(**document) for document in cursor]


# This route gets all comments of a specific post from the database
@router.get("/{blog_id}", operation_id="get_comments_of_post")
async def get_comments_for_blog_id(blog_id: str) -> list[Comment]:
    """
    This route handles the retrieval of all comments for a specific post from the database

    :param blog_id: the ID of the blog post to retrieve comments for
    :return: a list of Comment objects containing all comments for the specified blog post
    """

    # Retrieve comments for the specific blog post using the find method with a filter
    cursor = db.process.comment.find({'blog_id': blog_id})

    # Create a list of Comment objects by unpacking data from each document retrieved
    return [Comment(**document) for document in cursor]


# This route adds a comment to a specific post
@router.post("/{blog_id}", operation_id="add_comments_to_specific_post")
async def add_comment_to_post(blog_id: str, comment: Comment) -> Comment | None:
    """
    This route handles adding a new comment to a specific blog post

    :param blog_id: the ID of the blog post to add a comment to
    :param comment: the Comment object containing the details of the new comment
    :return: the added Comment object with its ID or None if the operation failed
    """

    # Convert Comment object to dictionary and add the blog_id
    comment_dict = comment.dict(by_alias=True)
    comment_dict['blog_id'] = blog_id

    # Insert the comment into the database
    insert_result = db.process.comment.insert_one(comment_dict)
    if insert_result.acknowledged:
        comment_dict['_id'] = str(insert_result.inserted_id)
        return Comment(**comment_dict)
    return None


# This route edits a comment by its ID
@router.put("/{blog_id}/{comment_id}", operation_id="edit_comment_by_id")
async def edit_comment(blog_id: str, comment_id: str, comment: Comment) -> Comment | None:
    """
    This route handles editing an existing comment by its ID

    :param blog_id: the ID of the blog post the comment belongs to
    :param comment_id: the ID of the comment to be edited
    :param comment: the Comment object containing the updated details of the comment
    :return: the updated Comment object or None if the operation failed
    """

    # Convert Comment object to dictionary and remove the _id field
    comment_dict = comment.dict(by_alias=True)
    del comment_dict['_id']

    # Update the comment in the database
    cursor = db.process.comment.update_one({'_id': comment_id, 'blog_id': blog_id}, {'$set': comment_dict})
    if cursor.modified_count > 0:
        updated_document = db.process.comment.find_one({'_id': comment_id})
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Comment(**updated_document)
    return None


# This route deletes a comment by its ID
@router.delete("/{blog_id}/{comment_id}", operation_id="delete_comment_by_id")
async def delete_comment(blog_id: str, comment_id: str) -> dict:
    """
    This route handles deleting a comment by its ID

    :param blog_id: the ID of the blog post the comment belongs to
    :param comment_id: the ID of the comment to be deleted
    :return: a dictionary message indicating the result of the delete operation
    """

    # Delete the comment from the database
    delete_result = db.process.comment.delete_one({'_id': comment_id, 'blog_id': blog_id})
    if delete_result.deleted_count > 0:
        return {"message": "Comment deleted successfully"}
    else:
        return {"message": "Comment not found"}
