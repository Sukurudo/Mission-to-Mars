#Import Dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

#Setup Flash
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    #Setup Databases in Mongo; 1 for data, 1 for images
    mars = mongo.db.mars.find_one() 
    mars_images = mongo.db.mars_images.find_one() 
    # Setting mars variable to mars in html
    return render_template("index.html", mars=mars, mars_images=mars_images) 

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_images = mongo.db.mars_images 
    mars_data, mars_images_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    mars_images.update({}, mars_images_data, upsert=True)
    # return "Scraping Successful!"
    return render_template("scraping.html")

if __name__ == "__main__":
    app.run()