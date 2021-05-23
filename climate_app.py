import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"        
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

##########precipitation is returning results; not closing session caused error of not being able to use the branches without restarting test
# Convert the query results to a dictionary using date as the key and prcp as the value. Using jupyter notebook queries as basis.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return a list of all precipitation"""
    print("Received API request")
    # Query all precip prcp
   # recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_precipitation = session.query(Measurement.date, func.max(Measurement.prcp)).\
                        filter(func.strftime("%Y-%m-%d", Measurement.date) > dt.date(2016, 8, 23)).\
                        group_by(Measurement.date).all()

    session.close()

    # create a dictionary for prcp info (date and prcp)
    all_rain = []
    for result in year_precipitation:
        precip_dict = {}
        precip_dict["date"] = year_precipitation[0]
        precip_dict["prcp"] = year_precipitation[1]
        all_rain.append(precip_dict)

    return jsonify(all_rain)

################stations is returning a result
@app.route("//api/v1.0/stations")
def stations():

    """Return a JSON list of stations from the dataset."""
    print("Received API request")

    # Query all stations
    stations = session.query(Station).all()

    session.close()

     # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station in stations:
        stations_dict = {}
        stations_dict["id"] = station.id
        stations_dict["station"] = station.station
        stations_dict["name"] = station.name
        stations_dict["latitude"] = station.latitude
        stations_dict["longitude"] = station.longitude
        stations_dict["elevation"] = station.elevation
        all_stations.append(stations_dict)

    return jsonify(all_stations)

########################################### tobs is returning results
@app.route("//api/v1.0/tobs")
def tobs():

    """Return a JSON list of temperature observations (TOBS) for the previous year"""
    print("Received API request")
    # Query the dates and temperature observations of the most active station for the last year of data.
    #recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of tobs_list
    tobs_list = []
    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result.date
        tobs_dict["station"] = result.station
        tobs_dict["tobs"] = result.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

########################################### 
@app.route("//api/v1.0/<start>")
def trip_1(start):

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    print("Received API request")
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    #finding year's worth of data as starting point; most recent date/endpoint : 2017-08-23
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    one_year =  dt.timedelta(days=365)
    start_data = start_date - one_year
    max_date = dt.date(2017, 8, 23)

    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_data).filter(Measurement.date <= max_date).all()
        
    session.close()

    #create a list
    trip = list(np.ravel(trip_data))

    return jsonify(trip)

########################################### 
@app.route("//api/v1.0/<start>/<end>")
def trip_2(start):

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    print("Received API request")

    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    #update last route with additional variable/function
    #finding year's worth of data as starting point; most recent date/endpoint : 2017-08-23
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    one_year =  dt.timedelta(days=365)
    start_data = start_date - one_year
    end_date = dt.datetime.strptime(start, "%Y-%m-%d")

    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_data).filter(Measurement.date <= max_date).all()
        
    session.close()

    #create a list
    trip = list(np.ravel(trip_data))

    return jsonify(trip)

#####################################end of work
if __name__ == '__main__':
    app.run(debug=True)