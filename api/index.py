app = Flask(__name__)

NEWS_API_KEY = os.getenv('NEWS_API_KEY', '101d2f72ecb3458aa8614823f25f8ad6')

def fetch_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",  # Get US news
        "pageSize": 10,   # Get top 10 articles
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            articles = response.json()["articles"]
            # Process and clean up the articles
            processed_articles = []
            for article in articles:
                # Create a simple summary by taking the first sentence of the description
                summary = article.get("description", "").split(". ")[0] + "."
                processed_articles.append({
                    "title": article.get("title", ""),
                    "summary": summary,
                    "url": article.get("url", ""),
                    "source": article.get("source", {}).get("name", ""),
                    "publishedAt": article.get("publishedAt", "")
                })
            return processed_articles
        return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    articles = fetch_news()
    return jsonify(articles)

if __name__ == "__main__":
    app.run(debug=True)