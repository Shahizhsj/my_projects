from fastapi import FastAPI, Depends, HTTPException
import schemas
from sqlalchemy.orm import Session
import models
from database import engine, session_local
import requests
from ml_model import ContentBasedRecommender
recommender = ContentBasedRecommender()


app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# Logging and sign-in section
@app.post('/signup', response_model=schemas.User_Sign)
def create_user(request: schemas.User_Sign, db: Session = Depends(get_db)):
    new = models.User(name=request.name, email=request.email, password=request.password)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@app.post('/login', response_model=schemas.User_Login)
def login(request: schemas.User_Sign, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == request.name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    if user.password != request.password:
        raise HTTPException(status_code=400, detail="Invalid password!")
    return {"name": user.name, "email": user.email, "message": "Login successful"}

#This function will do feteching of the news and stroing it in the database
@app.get('/allnews')
def all_news(db: Session = Depends(get_db)):
    api_key = "7d792db818424168969aa6112f89ab2b"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching news")

    news_data = response.json()

    for i in news_data['articles']:
        news = models.News(
            source=i['source']['name'],  # Changed from source_name to source
            author=i['author'],
            title=i['title'],
            description=i['description'],
            url=i['url'],
            urlToImage=i['urlToImage'],
            publishedAt=i['publishedAt'],
            content=i['content']
        )
        db.add(news)
        db.commit()
        db.refresh(news)
    return news_data['articles']

#this function will show the news fetched by the all_news function in the above
@app.get('/shownews')
def show_news(db:Session=Depends(get_db)):
    all_news=db.query(models.News).all()
    return all_news
#This function will update the databse that user has liked a news article and so that it can be used for future purpose
@app.post('/likes/{userid}/{interaction}/{postid}')
def user_likes(postid :int,interaction:str,userid:int,db:Session=Depends(get_db)):
    like=models.UserNewsInteraction(user_id=userid,post_id=postid,interaction_type=interaction)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like
#this functio is the startup function
@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    try:
        news_items = db.query(models.News).all()
        if news_items:
            recommender.fit(news_items)
    except Exception as e:
        print(f"Error initializing recommender: {e}")
    finally:
        db.close()
#this is the main function to recommend the news to the given user
@app.get('/recommend/{user_id}')
def recommend(user_id: int, n_recommendations: int = 5, db: Session = Depends(get_db)):
    # Fetch user interactions
    user_interactions = db.query(models.UserNewsInteraction).filter(
        models.UserNewsInteraction.user_id == user_id,
        models.UserNewsInteraction.interaction_type == 'Like'
    ).all()

    if not user_interactions:
        raise HTTPException(
            status_code=404,
            detail="No interaction history found for this user"
        )

    # Get the news items for recommendations
    news_items = db.query(models.News).all()

    # Update the recommender with latest news items
    recommender.fit(news_items)

    interacted_news_ids = [interaction.post_id for interaction in user_interactions]

    # Get user profile
    user_profile = recommender.get_user_profile(user_interactions)

    if user_profile is None:
        raise HTTPException(
            status_code=404,
            detail="Could not generate user profile"
        )

    # Get recommendations
    recommendations = recommender.recommend(
        user_profile=user_profile,
        n_recommendations=n_recommendations,
        exclude_news_ids=interacted_news_ids
    )

    return recommendations  # Add this return statement

