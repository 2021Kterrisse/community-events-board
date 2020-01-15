import os
from app import app
from flask import render_template, request, redirect




from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'events'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://dbUser:sWaN9SdDtqPFF3Wr@cluster0-stiba.mongodb.net/events?retryWrites=true&w=majority'

mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    #connect to the database
    collection = mongo.db.events
    #query the database to get all the events
    #store those events as a list of dictionaries called events
    events = list(collection.find({}))
    #print the events
    for event in events:
        print(event["event_name"])
        print(event["event_date"])
    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database
    collection = mongo.db.events
    # insert new data
    collection.insert({"event_name": "test", "event_date": "today"})
    # return a message to the user
    return "you added an event to the database!"

# need a get and a post method
@app.route('/results', methods = ["get", "post"])
def results():
    # store userinfo from the form
    user_info = dict(request.form)
    print(user_info)
    #store the event_name
    event_name = user_info["event_name"]
    print("the event name is ", event_name)
    #store the event_date
    event_date = user_info["event_date"]
    print("the event date is ", event_date)
    #connect to Mongo DB
    event_type = user_info["category"]
    print(event_type)
    collection = mongo.db.events
    #insert the user's input event_name and event_date to MONGO
    collection.insert({"event_name": event_name, "event_date": event_date, "event_type": event_type})
    #(so that it will continue to exist after this program stops)
    #redirect back to the index page
    return redirect('/index')

@app.route("/secret")
def secret():
    #connect to the database
    collection = mongo.db.events
    #delete everything from the database
    #invoke the delete_many method on the collection
    collection.delete_many({})
    return redirect('/index')

@app.route("/social")
def sorted():
    collection = mongo.db.events
    social = list(collection.find({"event_type": "social"}))
    print (social)
    return render_template('index.html', events = social)

@app.route("/work")
def work():
    collection = mongo.db.events
    work = list(collection.find({"event_type": "work"}))
    print (work)
    return render_template('index.html', events = work)

@app.route("/trips")
def trips():
    collection = mongo.db.events
    trips = list(collection.find({"event_type": "trips"}))
    print (trips)
    return render_template('index.html', events = trips)
    
@app.route("/school")
def school():
    collection = mongo.db.events
    school = list(collection.find({"event_type": "school"}))
    return render_template('index.html', events = school)
