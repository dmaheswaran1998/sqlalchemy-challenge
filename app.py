import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#saving the tables as classes
Base.classes.keys()
measurement=Base.classes.measurement
station=Base.classes.station
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
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"/api/v1.0/tobs<br/><br/>"
    

        f"/api/v1.0/startdate<br/>"
        f"For this route to work, a start date in format yyyy-mm-dd needs to be entered<br/><br/>"
        f"/api/v1.0/start/end<br/>"
        f"For this route to work, a start and end date in formate yyyy-mm-dd needs to be entered<br/><br/>"
    
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query measurement date and precipitation date 
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= '2016-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to the precipitation list. This creates key-value pairs with date as key value 
    # Precipitation is the valuye
    precip_list = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_list.append(precip_dict)

    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
   
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station ID and Name from station table"""
    # Query all stations
    results = session.query(station.station, station.name).all()

    session.close()

    # Store the query data as a list
    station_name = list(np.ravel(results))

    return jsonify(station_name)


@app.route("/api/v1.0/tobs")
def tobs():
   
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a date and temperature data from measurement table for most active station """
    # Query measurement temperatures and measurement observed temperatures 
    results1 = session.query (measurement.date, measurement.tobs).\
    filter(measurement.date >= '2016-08-23').\
    filter(measurement.station=="USC00519281").all()

    session.close()

    # Create a list from the results and jsonify the response 
    temperature_obs= list(np.ravel(results1))

    return jsonify(temperature_obs)


########################################
#IMPORTANT!!!!! For this URL to work, start date needs to be entered in the formal yyyy-mm-dd
########################################
@app.route("/api/v1.0/<start>")
def start(start):

    #create a session

    session=Session(engine)  

    #query 
    min = session.query(func.min(measurement.tobs)).\
    filter(measurement.date>=f'{start}').scalar()

    max = session.query(func.max(measurement.tobs)).\
    filter(measurement.date>=f'{start}').scalar()

    avg = session.query(func.avg(measurement.tobs)).\
    filter(measurement.date>=f'{start}').scalar()


    session.close()

    return jsonify(f'The min, max and average temperature from {start} to the end of the dataset is {min}, {max} and {avg} respectively')
########################################
#IMPORTANT!!!!! For this URL to work, start and end date needs to be entered in the formal yyyy-mm-dd
#######################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    #create a session

    session=Session(engine)  

    #query 
    min = session.query(func.min(measurement.tobs)).\
    filter(measurement.date>=f'{start}').\
    filter(measurement.date<=f'{end}').scalar()

    max = session.query(func.max(measurement.tobs)).\
    filter(measurement.date>=f'{start}').\
    filter(measurement.date<=f'{end}').scalar()

    avg = session.query(func.avg(measurement.tobs)).\
    filter(measurement.date>=f'{start}').\
    filter(measurement.date<=f'{end}').scalar()


    session.close()

    return jsonify(f'The min, max and average temperature between {start} and {end} is {min}, {max} and {avg} respectively')
  

if __name__ == '__main__':
    app.run(debug=False)