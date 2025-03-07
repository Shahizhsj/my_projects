# News Recommendation System

This project is a News Recommendation System built using FastAPI, SQLAlchemy, and a content-based recommendation algorithm. The system fetches news articles from the NewsAPI, stores them in a database, and provides personalized news recommendations to users based on their interactions.

## Features

- User signup and login functionality
- Fetch and store news articles from NewsAPI
- Display stored news articles
- Record user interactions with news articles (likes)
- Provide personalized news recommendations based on user interactions

## Project Structure

- `main.py`: The main FastAPI application file containing the API endpoints and logic.
- `schemas.py`: Schema definitions for request and response models using Pydantic.
- `ml_models.py`: Implementation of the content-based recommendation algorithm.
- `models.py`: SQLAlchemy models representing the database tables.
- `database.py`: Database connection setup and session management.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/news-recommendation-system.git
cd news-recommendation-system
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the database:

```bash
# Create the database tables
python -c "from database import engine, Base; Base.metadata.create_all(engine)"
```

5. Run the FastAPI application:

```bash
uvicorn main:app --reload
```

## API Endpoints

### User Authentication

- **Signup**: `POST /signup`
  - Request Body: `schemas.User_Sign`
  - Response: `schemas.User_Sign`

- **Login**: `POST /login`
  - Request Body: `schemas.User_Sign`
  - Response: `schemas.User_Login`

### News Management

- **Fetch and store news articles**: `GET /allnews`
  - Response: List of news articles

- **Show stored news articles**: `GET /shownews`
  - Response: List of stored news articles

### User Interactions

- **Record user interaction (like)**: `POST /likes/{userid}/{interaction}/{postid}`
  - Parameters: `userid` (int), `interaction` (str), `postid` (int)
  - Response: Recorded interaction

### Recommendations

- **Get personalized recommendations**: `GET /recommend/{user_id}`
  - Parameters: `user_id` (int), `n_recommendations` (int, optional, default=5)
  - Response: List of recommended news articles

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [NewsAPI](https://newsapi.org/)
- [scikit-learn](https://scikit-learn.org/)

## Contact

For any questions or inquiries, please contact [Your Name](shaikshair786@gmail.com).
