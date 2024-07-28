# Project Name

## Overview

This project is a comprehensive web application with various functionalities such as blogs, books, comments, contacts, experiences, links, newsletters, projects, subscribers, technology, and user management. It is organized into different directories for better modularity and maintainability.

## Architecture 

The project is structured into the following main directories:

- `src`
- `domain`
- `routes`
- `services`
- `template`
- `utils`

### src

Contains the main application files for different modules.

- `database`: Database connection and ORM setup.
- `blog.py`: Blog-related functionalities.
- `book.py`: Book-related functionalities.
- `contact.py`: Contact form and related operations.
- `experiences.py`: User experiences handling.
- `newsletter.py`: Newsletter management.
- `subscriber.py`: Subscriber management.

### domain

Contains the domain models and logic.

- `blog.py`: Domain logic for blogs.
- `contact.py`: Domain logic for contact information.
- `newsletter.py`: Domain logic for newsletters.
- `subscriber.py`: Domain logic for subscribers.
- `token.py`: Token management for authentication.
- `token_data.py`: Token data models.
- `user_in_db.py`: User data models for the database.

### routes

Contains the routing logic for the web application.

- `admin.py`: Admin-related routes.
- `blog.py`: Routes for blog functionalities.
- `book.py`: Routes for book functionalities.
- `contact.py`: Routes for contact form.
- `email.py`: Email-related routes.
- `index.py`: Main index routes.
- `login.py`: Routes for user login.
- `newsletter.py`: Routes for newsletters.
- `subscriber.py`: Routes for subscribers.

### services

Contains the service layer for handling business logic.

- `blog_notification.py`: Service for blog notifications.
- `db.py`: Database service.
- `email_confirm.py`: Service for email confirmation.
- `emails.py`: Email handling services.
- `newsletters.py`: Service for managing newsletters.
- `security.py`: Security-related services.

### template

Contains the email templates used in the application.

- `blog_notifications.py`: Template for blog notifications.
- `confirmation_newsletter_email.py`: Template for newsletter confirmation emails.
- `confirmation_registered_user.py`: Template for registered user confirmation emails.
- `email_template.py`: Base template for emails.
- `newsletter_body.py`: Template for newsletter body content.
- `registered_user.py`: Template for registered user emails.

### utils

Contains utility scripts and functions.

- `domain_to_txt.py`: Utility for domain to text conversion.
- `__main__.py`: Main entry point for utility scripts.
- `env.py`: Environment variable handling.
- `output.txt`: Output handling utility.
- `tags_metadata.py`: Metadata for API tags.

## Environment Variables

The project uses environment variables for configuration. An example `.env-template` file is provided.

- `.env`: Actual environment variables file.
- `.env-template`: Template for environment variables.

## Other Files

- `.gitignore`: Git ignore file.
- `danilojezernik-api.iml`: Project configuration file.
- `Dockerfile`: Docker configuration for containerization.
- `README.md`: Project documentation.
- `requirements.txt`: Python dependencies.
