from flask import Flask, render_template
import json
import feedparser
import globalvoices
from pymongo import MongoClient
import logging

app = Flask(__name__)
c = MongoClient('localhost',27017)

mongo_stories = c.gv.stories

@app.route("/")
def index():
    return render_template("stories.html",
        country_list_json_text=json.dumps(globalvoices.country_list())
    )

@app.route("/country/<country>")
def country(country):
	if mongo_stories.find({'country':country}).count > 0:	
		stories = mongo_stories.find({'country':country})
		
	else:
    	stories = globalvoices.recent_stories_from( country )
    	for story in stories:
    		mongo_stories.insert(story)
    		
    return render_template("stories.html",
        country_list_json_text=json.dumps(globalvoices.country_list()),
        country_name=country,
        stories=stories
    )

if __name__ == "__main__":
    app.debug = True
    app.run()
