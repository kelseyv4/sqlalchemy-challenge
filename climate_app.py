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

##########precipitation is having errors: 
# Convert the query results to a dictionary using date as the key and prcp as the value. Using jupyter notebook queries as basis.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return a list of all precipitation"""
    print("Received API request")
    # Query all precip prcp
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_precipitation = session.query(Measurement.date, func.max(Measurement.prcp)).\
                        filter(func.strftime("%Y-%m-%d", Measurement.date) > dt.date(2016, 8, 23)).\
                        group_by(Measurement.date).all()

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

#################tobs is returning a result, renamed the reused functions/setup to stop an error from using the same exact thing
@app.route("//api/v1.0/tobs")
def tobs():

    """Return a JSON list of temperature observations (TOBS) for the previous year"""
    print("Received API request")
    # Query the dates and temperature observations of the most active station for the last year of data.
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= one_year_ago).all()

    # Create a dictionary from the row data and append to a list of tobs_list
    tobs_list = []
    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result.date
        tobs_dict["station"] = result.station
        tobs_dict["tobs"] = result.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)