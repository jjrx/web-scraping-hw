from flask import Flask, render_template, redirect
import pymongo
import scrape_mars
from bson.json_util import dumps

# create instance of Flask app
app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.mars_info

@app.route('/')
def index():
    mars_info = collection.find_one()
    return render_template("index.html", mars_info=mars_info)

@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
