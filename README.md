# **FastAPI Project**

This is a FastAPI project with various domain models, routes, and services configured for a web application. It includes functionality for writing model fields to a TypeScript-compatible format for frontend use.

## **Table of Contents**

- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Writing Fields to output.txt](#writing-fields-to-outputtxt)

## **Installation**

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    ```

2. Navigate to the project directory:
    ```bash
    cd <your-file-clone-repository>
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## **API Endpoints**
The project includes the following routes:

* /index
* /blog
* /comments
* /experiences
* /links
* /email
* /projects
* /user
* /login
* /register
* /contact
* /newsletter
* /subscriber

Each route is prefixed with its corresponding path and tagged for easier organization in the OpenAPI documentation.

## **Models**

The project includes several Pydantic models defined in the src.domain package:

* Blog
* Experiences
* Contact
* User
* Links
* Projects
* Subscriber
* Newsletter
* Comment

## **Writing Fields to output.txt**
This project includes a script to document the field names and types of the models and write them to output.txt for frontend usage.

To use this feature:

1. Run the main script
2. When prompted, type `y` to drop and seed the database if needed. 
3. When prompted, type `y` to write the document.

The script will generate an `output.txt` file with the following format:

```typescript
/* tslint:disable */
/* eslint-disable */

export interface Blog {
   '_id'?: string;
   naslov: string;
   kategorija: string;
   // and others
}

/* tslint:disable */
/* eslint-disable */

export interface Experiences {
   '_id'?: string;
   title: string;
   stack: string;
   // and others
}

// Other models will follow the same pattern
```