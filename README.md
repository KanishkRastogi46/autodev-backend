# Backend for final year project

## Steps to follow before starting the project
- ### Clone the repo
  ```shell
  git clone https://github.com/KanishkRastogi46/autodev-backend
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
- Create a MySQL database on cloud and store its credentials in .env file and also download the .pem at the root folder
- Also create an API key to integrate Google Gemini Api on [Google ai studio](https://aistudio.google.com/)
- Run your app using
  ```shell
  uvicorn main:app --reload
  ```
- Your app is running on port 8000


## Users route ("/users")
1. ### "/"- for getting all users
2. ### "/register"- for registering users
