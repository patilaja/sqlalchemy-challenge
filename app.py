#Import dependecies
#All DB queries are in dbFunction file
from dbFunction import *
from flask import jsonify,render_template, json

#Take care of page not found  
@app.errorhandler(404) 
  
# Use inbuilt function which takes error as parameter 
def not_found(e): 
  #redirect to home page - we can always show custom page
  return render_template("home.html", title="Honolulu API") 

#Define routes - this is used for assignment purpose to show output in JSON format
@app.route("/")
@app.route("/api/v1.0/")
def homepage():
    #Defsult page that lists all API and corresponding URL
    return render_template("home.html", title="Honolulu API")

@app.route("/api/v1.0/precipitation")
def percipitation():
    #Get precipitation results
    precipitation_dict = fpercipitation()
    #Return json output
    return jsonify(precipitation_dict) 

@app.route("/api/v1.0/stations")
def stations():
    #Get list of stations
    station_list = fstations()
    #Return json output
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #Get temperature observations
    tobs = ftobs()
    #Return json output
    return jsonify(tobs) 

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None,end=None):
    #Get min.avg and max temperatures for a start date or a date range of start and end date
    calc_temp = fstart_end(start=start,end=end )
    #Return json output
    return jsonify(calc_temp) 

#Webpage routs - add w prefic for all routes and linking to site page to show output
@app.route("/api/v1.0/wprecipitation")
def wpercipitation():
    #Get precipitation
    precipitation_dict = fpercipitation()
    #Display results in precipitation web page
    return render_template("precipitation.html", title="Precipitations API", per_dct = precipitation_dict, perc=json.dumps(precipitation_dict)) 

@app.route("/api/v1.0/wstations")
def wstations():
    #Get list of stations
    station_list = fstations()
    #Display results in stations web page
    return render_template("stations.html", title="Stations API", stations=station_list)

@app.route("/api/v1.0/wtobs")
def wtobs():
    #Get temperature observations
    tobs = ftobs()
    #Display results in tobs web page
    return render_template("tobs.html", title="Most Active Station Observed Temperature API", tobs = tobs, tobs_json=json.dumps(tobs)) 

@app.route("/api/v1.0/w/<start>")
@app.route("/api/v1.0/w/<start>/<end>")
def wstart_end(start=None,end=None):
    #Get min,avg and max temperatures for a start date or a date range of start and end date
    calc_temp = fstart_end(start=start,end=end )
    #Display results in temperature web page
    return render_template("temperature.html", title="Temperature API", calc_temp = calc_temp, calc=json.dumps(calc_temp), startdate=start, enddate=end) 

#Application set to debug mode - update debug flag = Flase once testing is done
if __name__ == '__main__':
    app.run(debug=True)