import os

from dotenv import load_dotenv

load_dotenv()
PORT = int(os.getenv('PORT'))

# MongoDB connections
DB_MAIN = str(os.getenv('DB_MAIN'))
DB_PROCESS = str(os.getenv('DB_PROCESS'))

# Fast API security
ALGORITHM = str(os.getenv('ALGORITHM'))
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# User in database
USERNAME = str(os.getenv('USERNAME'))
EMAIL = str(os.getenv('EMAIL'))
PASSWORD = str(os.getenv('PASSWORD'))

# GitHub
GITHUB = str(os.getenv('GITHUB'))
GITHUB_TOKEN = str(os.getenv('GITHUB_TOKEN'))

# Newsletter
DOMAIN = str(os.getenv('DOMAIN'))
DOMAIN_REGISTER = str(os.getenv('DOMAIN_REGISTER'))

# TESTING
EMAIL_1 = str(os.getenv('EMAIL_1'))
EMAIL_2 = str(os.getenv('EMAIL_2'))
