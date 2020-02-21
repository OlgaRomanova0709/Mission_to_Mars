from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_information

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route("/")
def index():

    news = mongo.db.news.find_one()

    featured = mongo.db.featured.find_one()

    hemi_list = list(mongo.db.hemi_dict.find())

    tableD = mongo.db.tableD.find_one()

    return render_template("index.html", news=news,featured=featured,hemi_list=hemi_list,tableD=tableD)

@app.route("/scrape")
def scrape():
    news = mongo.db.news
    news_data = mars_information.scrape_news()
    news.update({}, news_data, upsert=True)
    
    featured = mongo.db.featured
    featured_data = mars_information.scrape_featured()
    featured.update({}, featured_data, upsert=True)
  
    hemi_data = mars_information.scrape_hemi()
    mongo.db.hemi_dict.drop()
    for i in hemi_data:
        mongo.db.hemi_dict.insert(i)

    tableD = mongo.db.tableD
    table_data = mars_information.scrape_table()
    tableD.update({}, table_data, upsert=True)
    
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
