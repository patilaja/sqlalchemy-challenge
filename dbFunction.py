#Import dependecies
from flask import Flask, jsonify,render_template, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func

import datetime as dt
import numpy as np

#Get app
app = Flask(__name__)

#Configure path for sqlite - normally should be ion config or environment
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Resources/hawaii.sqlite'
db = SQLAlchemy(app)

#Get db table reflection 
Base = automap_base()
Base.prepare(db.engine,reflect=True)

#Save references of the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Function purpose: Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
#Return the JSON representation of your dictionary.
def fpercipitation():
    #Get the max date 
    max_date=db.session.query(func.max(Measurement.date)).first()
    max_date =max_date[0]

    #Calculate the date 1 year ago from today. There are 365 days in a year
    one_year_ago=dt.datetime.strptime(max_date, "%Y-%m-%d")-dt.timedelta(days=365)

    #Perform a query to retrieve the data and precipitation scores
    precipitations = db.session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    #Convert list of tuples into normal list
    precipitation_dict = dict(precipitations)

    #Return query results in dictionary form
    return precipitation_dict

#Function purpose: Return a JSON list of stations from the dataset 
def fstations():
    #Get Station List
    station_list= db.session.query(Measurement.station).distinct().all()

    #Convert list of tuples into normal list
    station_list = list(np.ravel(station_list))

    #Return query results in a list form
    return station_list

#Function purpose: Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.    
def ftobs():
    #Get the max date 
    max_date=db.session.query(func.max(Measurement.date)).first()
    max_date =max_date[0]

    #Calculate the date 1 year ago from today. There are 365 days in a year
    one_year_ago=dt.datetime.strptime(max_date, "%Y-%m-%d")-dt.timedelta(days=365)

    #Get most active station
    active_stations=db.session.query(Measurement.station,func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).first()
    active_station =active_stations[0]
    
    #Perform a query to retrieve the data and precipitation scores
    tobs = db.session.query(Measurement.date,Measurement.tobs).filter(Measurement.station== active_station).filter(Measurement.date >= one_year_ago).all()
    print(tobs)
    #Return query results 
    return tobs

#Function purpose: Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#Assumption-user will enter correct date format
def fstart_end(start=None,end=None):
    #Check if start and end date is entered
    if start and end :
        #Use start and end date condition 
        calc_temp = db.session.query(func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs),1), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
 
        #Check if only start is entered
    elif start and not end:
        calc_temp = db.session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    #Return query results 
    return calc_temp