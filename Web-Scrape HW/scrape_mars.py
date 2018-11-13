from bs4 import BeautifulSoup 
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import tweepy
from config import (consumer_key,
                    consumer_secret,
                    access_token,
                    access_token_secret)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
import pandas as pd
#import pymongo
from pprint import pprint
#from flask import Flask, render_template

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
#db = client.

def scrape():

    #!which chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    # Retrieve page with the requests module
    #response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(html, 'html.parser')
    news_p_list = []
    news_title_list = []

    results = soup.find_all('li', class_ ='slide')

    for result in results:
        newstitle = result.find('div',class_='content_title')
        news_title= newstitle.a.text
        news_p = result.find('div', class_ = 'article_teaser_body').text
        news_p_list.append(news_p)
        news_title_list.append(news_title)

        #print(news_title)
        #print("______")
        #print(news_p)
        #print("______")
    print(news_title_list[0])
    print(news_p_list[0])

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find('div',class_='carousel_items').a
    print(soup.find('div',class_='carousel_items').article['style'].split("/",1)[1].rstrip("');"))
    featured_image_url = "https://www.jpl.nasa.gov/" +  soup.find('div',class_='carousel_items').article['style'].split("/",1)[1].rstrip("');")
    #featured_image_url = "https://www.jpl.nasa.gov" + results['data-fancybox-href']
    print(featured_image_url)

    tweets = api.user_timeline('MarsWxReport',count=1)
    mars_weather = []
    for tweet in tweets:
        pprint(tweet['text'])
        mars_weather.append(tweet['text'])
    print(mars_weather)

    target_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(target_url)
    tables =tables[0]
    tables = tables.rename(columns={0: "Info", 1:"Value"})
    tables.set_index('Info', inplace=True)
    weather_stuff = tables.to_dict()
    weather_stuff

    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
        {"title": "Schiaparelli Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
        {"title": "Syrtis Major Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
        {"title": "Valles Marineris Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"},
    ]
    scraped_dict = {"Mars_news_title":news_title_list[0],"Mars_news_p":news_p_list[0],"Mars_images":featured_image_url,"Mars_tweets":mars_weather,"Mars_stats": weather_stuff,"Mars_hemi": hemisphere_image_urls}
    return scraped_dict


