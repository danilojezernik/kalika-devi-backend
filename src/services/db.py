from pymongo import MongoClient

from src import env

from src.database.blog import blog
from src.database.book import book
from src.database.contact import contact
from src.database.experiences import experiences
from src.database.links import links
from src.database.newsletter import newsletter
from src.database.projects import projects
from src.database.subscriber import subscriber
from src.database.technology import technology
from src.database.user import user
from src.database.comments import comments

client = MongoClient(env.DB_MAIN)
process = client[env.DB_PROCESS]


def drop():
    process.blog.drop()
    process.links.drop()
    process.experiences.drop()
    process.contact.drop()
    process.projects.drop()
    process.newsletter.drop()
    process.subscriber.drop()
    process.comments.drop()
    process.book.drop()
    process.technology.drop()
    pass


def drop_user():
    process.user.drop()
    pass


def seed():
    process.blog.insert_many(blog)
    process.links.insert_many(links)
    process.experiences.insert_many(experiences)
    process.contact.insert_many(contact)
    process.projects.insert_many(projects)
    process.newsletter.insert_many(newsletter)
    process.subscriber.insert_many(subscriber)
    process.comments.insert_many(comments)
    process.book.insert_many(book)
    process.technology.insert_many(technology)
    pass


def seed_user():
    process.user.insert_many(user)
    pass
