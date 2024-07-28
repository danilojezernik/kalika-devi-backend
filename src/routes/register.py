"""
Routes:
1. Register new user - Register a new user and store their data in the database.
2. Confirm registration - Confirm a user's registration via a confirmation link.
"""

from datetime import timedelta

from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import RedirectResponse

from src import env
from src.domain.user import User
from src.services import emails, db, security
from src.services.security import make_hash
from src.template import registered_user, confirmation_registered_user

router = APIRouter()


@router.post("/", operation_id='register_new_user')
async def register_new_user(user_data: User):
    """
    Handles user registration by creating a new user and storing the data in the database.

    :param user_data: Registration data containing username, email, full_name, and password.
    :return: The registered user data.
    """
    try:
        # Hash the user's password before storing it
        hashed_password = make_hash(user_data.hashed_password)

        # Create a User object with the provided data
        user_data = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            disabled=False,
            confirmed=user_data.confirmed,
            registered=user_data.registered,
            blog_notification=user_data.blog_notification,
        )

        # Save the user to the database
        db.process.user.insert_one(user_data.dict(by_alias=True))

        # Generate the HTML body for the email using the provided data
        body = registered_user.html(full_name=user_data.full_name, username=user_data.username, email=user_data.email)

        # Attempt to send the registration email
        if not emails.send_email(email_from=user_data.email, subject='New user registered on danilojezernik.com',
                                 body=body):
            # If sending fails, raise an HTTPException with a 500 status code and a detail message
            raise HTTPException(status_code=500, detail='Email not sent')

        # Create an access token with a short expiration time
        token = security.create_access_token(data={'user_id': user_data.id}, expires_delta=timedelta(minutes=10))

        # Generate the confirmation email's HTML content
        body = confirmation_registered_user.html(link=f'{env.DOMAIN}/register/registered/{token}',
                                                 full_name=user_data.full_name)

        # Send the confirmation email to the subscriber
        if not emails.send_confirm(email_to=user_data.email,
                                   subject='DaniloJezernik.com | Potrdite svojo registracijo ♥', body=body):
            return HTTPException(status_code=500, detail="Email not sent")

        # Return a success response
        return {'registered_user'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {e}")


# CLIENT CONFIRMING EMAIL FOR REGISTRATION
@router.get("/registered/{token}")
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
    try:
        # Extract the user_id from the confirmation token
        payload = await security.get_payload(token=token)

        # Mark the subscriber as confirmed in the database
        db.process.user.update_one({"_id": payload['user_id']}, {"$set": {"registered": True}})

        return RedirectResponse(url=f'{env.DOMAIN_REGISTER}/', status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")