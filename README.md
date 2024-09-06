
# Mediterranean Cuisine RESTful API

## Overview

This project is a RESTful API designed to supply a variety of Mediterranean cuisine recipes. Built using FastAPI, the API allows users to create and manage their accounts, authenticate, and access a collection of recipes. The API supports various functionalities such as retrieving all recipes, adding new recipes, searching for recipes by ingredients or country, and managing user accounts. The project was made for academic purposes.

<br>
<br>
![Mediterranean](medi)

## Features

- **User Management:**
  - Create a new user account.
  - Retrieve user details by user ID.
  
- **Authentication:**
  - User login to obtain an access token.
  
- **Recipe Management:**
  - Retrieve all recipes.
  - Add a new recipe.
  - Search recipes by ingredients.
  - Retrieve recipes based on the country of origin.

## Endpoints

### 1. User Endpoints

- **Create a New User**
  - **`POST /users`**
  - Creates a new user with the specified email and password.
  - **Request Body:** `schemas.User`
  - **Response:** Created user details.
  
- **Get User by ID**
  - **`GET /users/{id}`**
  - Retrieves a user by their unique ID.
  - **Response:** User details if found, otherwise a 404 error.

### 2. Authentication Endpoints

- **User Login**
  - **`POST /login`**
  - Authenticates the user and returns a JWT token.
  - **Request Body:** `OAuth2PasswordRequestForm`
  - **Response:** Access token and token type.

### 3. Recipe Endpoints

- **Get All Recipes**
  - **`GET /recipes`**
  - Retrieves all available recipes from the database.
  - **Response:** List of all recipes.

- **Add a New Recipe**
  - **`POST /recipes`**
  - Adds a new recipe to the database.
  - **Request Body:** `schemas.Recipe`
  - **Response:** The newly created recipe.

- **Search Recipes by Ingredients**
  - **`GET /recipes/search`**
  - Searches for recipes that contain specific ingredients.
  - **Query Parameters:** Comma-separated list of ingredients.
  - **Response:** List of recipes that match the search criteria.

- **Get Recipes by Country**
  - **`GET /recipes/country/{country}`**
  - Retrieves recipes originating from a specified country.
  - **Response:** List of recipes from the specified country.
