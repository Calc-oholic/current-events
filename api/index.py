from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)
NEWS_API_KEY = '101d2f72ecb3458aa8614823f25f8ad6'

def fetch_news():
    # Fetch general headlines
    url = "https://newsapi.org/v2/top-headlines"
    categories = ["general", "business", "technology", "science", "health", "sports"]
    all_articles = []
    
    for category in categories:
        params = {
            "country": "us",
            "category": category,
            "pageSize": 5,  # 5 articles per category
            "apiKey": NEWS_API_KEY
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                articles = response.json()["articles"]
                for article in articles:
                    summary = article.get("description", "").split(". ")[0] + "."
                    all_articles.append({
                        "title": article.get("title", ""),
                        "summary": summary,
                        "url": article.get("url", ""),
                        "source": article.get("source", {}).get("name", ""),
                        "publishedAt": article.get("publishedAt", ""),
                        "category": category,
                        "content": article.get("content", "")
                    })
        except Exception as e:
            print(f"Error fetching {category} news: {e}")
    
    return all_articles

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    articles = fetch_news()
    return jsonify(articles)

@app.route('/api/quiz', methods=['POST'])
def generate_quiz():
    data = request.json
    article = data.get('article')
    questions = [
        {
            "question": f"What is the main topic of this {article['category']} article?",
            "answer": article['title']
        },
        {
            "question": "Which news source published this article?",
            "answer": article['source']
        },
        {
            "question": "When was this article published?",
            "answer": article['publishedAt']
        }
    ]
    return jsonify(questions)

if __name__ == "__main__":
    app.run(debug=True)
