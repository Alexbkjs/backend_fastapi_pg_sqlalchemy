# 🚀 Backend FastAPI with PostgreSQL and SQLAlchemy

Backend built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. This project serves as a foundation for modern web applications and APIs.
`node_js_mock_data` folder contains genereta_data.js nodejs script to generate `initDataRaw` that can be verified on back end.

## 🛠️ Features

- **FastAPI**: High-performance Python web framework for building APIs.
- **PostgreSQL**: Powerful, open-source relational database.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Alembic**: Database migrations tool for SQLAlchemy.

## 📝 Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.8+**
- **PostgreSQL**
- **Git**

## 📦 Installation and Setup

Follow these steps to clone the repository and set up the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Alexbkjs/backend_fastapi_pg_sqlalchemy.git
cd backend_fastapi_pg_sqlalchemy
```
### 2. Create and Activate a Virtual Environment

For Unix/macOS:

```bash
python3 -m venv venv
source env/bin/activate
```

For Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up the PostgreSQL Database

- #### 4.1. Create a PostgreSQL database:

```bash
createdb your_database_name
```

- #### 4.2. Update the Database Connection Settings:
Update the .env file with your PostgreSQL credentials:


```bash
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/your_database_name
```

#### 5. Apply Database Migrations

```bash
alembic upgrade head
```


#### 6. Run the Application

```bash
uvicorn main:app --reload
```
The API will be available at http://127.0.0.1:8000. 

#### 7. To be able to access your locally running application remotly use serveo, ngrok, etc.

```bash
ssh -R subdomainYouLike:80:localhost:8000 serveo.net
```

## 📚 Project Structure


```bash
backend_fastapi_pg_sqlalchemy/
├── app/
│   ├── api/               # API routes
│   ├── database.py/       # Database models and sessions
│   ├── models.py/         # SQLAlchemy models
│   └── schemas.py/        # Pydantic schemas
├── alembic/               # Alembic migrations
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── main.py                # FastAPI entry point
└── README.md              # Project documentation
```
## ✅ Running Tests
To run tests, you can use pytest:

```bash
pytest
```
## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue.

1. - Fork the repository.
2. - Create a new branch (git checkout -b feature-branch).
3. - Commit your changes (git commit -m 'Add some feature').
4. - Push to the branch (git push origin feature-branch).
5. - Open a Pull Request.

## 🛡️ License
This project is licensed under the Apache License. See the LICENSE file for more details.

## 🌟 Acknowledgements
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
