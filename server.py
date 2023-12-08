from flask import Flask, request
from db import coll_rules, coll_history
from actions import record_video, screenshot, check_time
from datetime import date, datetime

import os

# Create flask server
app = Flask(__name__)

@app.route('/urls', methods=['POST'])
def receive_urls():

    # Today's date
    today_date = str(date.today())

    # Check if folder by today's date name exist, if not it is creates one
    try:
        os.mkdir(today_date)
    except:
        pass

    # The URLS which being sent by the browser extension    
    urls = request.json['urls']

    # Query the collection and retrieve all documents
    cursor = coll_rules.find({})

    # Iterate over the documents and print the field value
    for document in cursor:
        url = document['url']
        start_time = datetime.now() # Start time of the browsing
        action_used = None # Action which used is default to None

        if url in str(urls): # Check if URL is in the system's rules
            
            # Check if need to record video
            if (document['action'] == "record_video") and (document['state'] == "enable") and (check_time(document['from'], document['to'])):
                record_video(website=url, date=today_date)
                action_used = "record_video"

            # Check if need to screenshot
            elif (document["action"] == "screenshot") and (document["state"] == "enable") and (check_time(document['from'], document['to'])):
                screenshot(website=url, date=today_date)
                action_used = "screenshot"

        end_time = datetime.now() # End time of browsing 

        # Add information to history database
        coll_history.insert_one({"website": str(urls),
                                "action": action_used,
                                "time": f"{start_time} - {end_time}"})


    return 'OK'

# function which run the server
def run_flask_app():
    app.run()
