# Import necessary modules and libraries
import httpx  # Library for making HTTP requests
from fastapi import APIRouter, HTTPException   # Importing APIRouter from FastAPI framework

# Importing environment variables from src folder
from src import env

# Creating an instance of APIRouter
router = APIRouter()


# Route handler to fetch GitHub repositories
@router.get('/')
async def get_repo():
    """
    Route handler to fetch GitHub repositories of a specific user.

    Returns:
        dict: A dictionary containing the fetched repositories.
    """
    per_page = 30  # Number of repositories per page
    repos = []  # List to store all fetched repositories
    page = 1  # Initial page number

    headers = {
        'Authorization': f'token {env.GITHUB_TOKEN}'
    }

    async with httpx.AsyncClient() as client:
        while True:
            url = f"https://api.github.com/users/{env.GITHUB}/repos?per_page={per_page}&page={page}"
            response = await client.get(url, headers=headers)

            # Check if the response status code is not 200 (OK)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"Error fetching repositories: {response.text}")

            try:
                page_repos = response.json()
            except ValueError:
                raise HTTPException(status_code=500, detail="Invalid JSON response from GitHub API")

            # Check if the response contains repositories
            if not page_repos:
                break  # Exit the loop if there are no more repositories

            # Filter public repositories and add them to the list
            public_repos = [repo for repo in page_repos if not repo.get('private')]
            repos.extend(public_repos)

            # Increment page number for the next set of repositories
            page += 1

    # Returning the fetched repositories as a dictionary
    return {'repos': repos}