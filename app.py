from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_information

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    news = mongo.db.news.find_one()

    featured = mongo.db.featured.find_one()

    weather_news = mongo.db.weather_news.find_one()

    hemi_list = list(mongo.db.hemi_dict.find())

    table_mars = list(mongo.db.table_m.find())
    return render_template("index.html", news=news,featured=featured,weather_news=weather_news,hemi_list=hemi_list,table_mars=table_mars)

@app.route("/scrape")
def scraper():
    news = mongo.db.news
    news_data = mars_information.scrape_news()
    news.update({}, news_data, upsert=True)
    
    featured = mongo.db.featured
    featured_data = mars_information.scrape_featured()
    featured.update({}, featured_data, upsert=True)

    weather_news = mongo.db.weather_news
    weather_news_data = mars_information.scrape_weather()
    weather_news.update({}, weather_news_data, upsert=True)
    
    hemi_data = mars_information.scrape_hemi()
    mongo.db.hemi_dict.drop()
    for i in hemi_data:
        mongo.db.hemi_dict.insert(i)
    
    table_data = mars_information.scrape_table()
    mongo.db.table_m.drop()
    for i in table_data:
        mongo.db.table_m.insert(i)
    
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
