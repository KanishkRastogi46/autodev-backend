# Backend for final year project using FastApi and frontend using Next.js

## Steps to follow before starting the project
- ### Clone the repo
  ```shell
  git clone https://github.com/KanishkRastogi46/autodev-backend.git
  ```
- ### Create virtual environment
  ```shell
  python -m venv .venv
  ```
- ### Activate virtual environment
  ```shell
  ./.venv/Scripts/Activate.ps1
  ```
- ### Install required packages
  ```shell
  pip install -r requirements.txt
  ```
- Create .env file at the root folder
- Create a PostgreSQL database on cloud and store its credentials in .env file and also download the .pem at the root folder
- Also create an API key to integrate Google Gemini Api on [Google ai studio](https://aistudio.google.com/)
- Run your app using
  ```shell
  uvicorn main:app --reload
  ```
- Your app is running on port 8000


## Users 
- ### route ("/users")
  1. ### "/"- for getting all users
  2. ### "/register"- for registering users
- ### model
  1. ### Users model
  2. ### Fields- user_id, email, password, profile_pic, is_verified

## For more details about api routes [visit](https://autodev-backend.onrender.com/docs) here
