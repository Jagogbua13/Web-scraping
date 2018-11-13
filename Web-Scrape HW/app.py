from flask_pymongo import PyMongo
from pprint import pprint
from flask import Flask, render_template, redirect
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] =  "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route('/')
def index():

    mars = mongo.db.collection.find_one()
    return render_template("index.html",mars = mars)

@app.route('/scrape')
def scrape_data():
    # title = scrape.Mars_news_title()
    # news_p = scrape.Mars_news_p
    # mars_img = scrape.Mars_images
    # mars_tweet = scrape.Mars_tweets
    # mars_stats = scrape.Mars_stats
    # mars_hemi = scrape.Mars_hemi

    # mars_data = {"news_title":title,
    # "news_text":news_p,
    # "mars_img":mars_img,
    # "mars_tweets":mars_tweet,
    # "mars_weather":mars_stats,
    # "mars_hemi":mars_hemi }
    mars_data = scrape_mars.scrape()
    

    mongo.db.collection.update({},mars_data,upsert = True)
    return redirect("/",code=302)


if __name__ == "__main__":
    app.run(debug=True)
