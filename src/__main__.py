# Fast API imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import env
# Import domain for output.txt
from src.domain.blog import Blog
from src.domain.book import Book
from src.domain.contact import Contact
from src.domain.newsletter import Newsletter
from src.domain.subscriber import Subscriber
from src.domain.user import User
# Imported routes
from src.routes import index, blog, login, user, contact, newsletter, \
    subscriber, book
from src.services import db
from src.tags_metadata import tags_metadata
from src.utils.domain_to_txt import write_fields_to_txt

app = FastAPI(openapi_tags=tags_metadata)

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(index.router, prefix='/index', tags=['Index'])
app.include_router(blog.router, prefix='/blog', tags=['Blog'])
app.include_router(book.router, prefix='/book', tags=['Book'])

app.include_router(user.router, prefix='/user', tags=['User'])
app.include_router(login.router, prefix='/login', tags=['Login'])

app.include_router(contact.router, prefix='/contact', tags=['Contact'])
app.include_router(newsletter.router, prefix='/newsletter', tags=['Newsletter'])
app.include_router(subscriber.router, prefix='/subscriber', tags=['Subscriber'])

if __name__ == '__main__':

    # Confirm if you want to drop and seed database
    yes = input('Type "y" if you want to run drop and seed: ').strip().lower()
    if yes == 'y':
        print('drop() and seed() initialized')
        db.drop()
        db.seed()
    else:
        print('Database drop and seed skipped')

    # Confirm if you want to drop and seed users database
    drop_user = input('If you want to drop user type "y": ').strip().lower()
    if drop_user == 'y':
        db.drop_user()
        db.seed_user()
    else:
        print('User drop and seed skipped')

    # Confirm if you want to write fields to output.txt
    yes_doc = input('Type "y" if you want to write the document and press enter: ').strip().lower()
    if yes_doc == 'y':
        print('Writing fields to output.txt...')
        write_fields_to_txt(
            [Blog, Contact, Newsletter, Subscriber, User, Book])
        print('Done! Fields have been written to output.txt')
    else:
        print('Document writing aborted')

    uvicorn.run(app, host="127.0.0.1", port=env.PORT)
