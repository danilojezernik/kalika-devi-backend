from pymongo import MongoClient

from src import env

from src.database.blog import blog
from src.database.book import book
from src.database.contact import contact
from src.database.newsletter import newsletter
from src.database.subscriber import subscriber
from src.database.user import user

client = MongoClient(env.DB_MAIN)
process = client[env.DB_PROCESS]


def drop():
    process.blog.drop()
    process.contact.drop()
    process.newsletter.drop()
    process.subscriber.drop()
    process.book.drop()
    pass


def drop_user():
    process.user.drop()
    pass


def seed():
    process.blog.insert_many(blog)
    process.contact.insert_many(contact)
    process.newsletter.insert_many(newsletter)
    process.subscriber.insert_many(subscriber)
    process.book.insert_many(book)
    pass


def seed_user():
    process.user.insert_many(user)
    pass
