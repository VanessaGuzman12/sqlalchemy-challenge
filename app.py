import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)
print(Base.classes.keys())

Measurement = Base.classes.measurement
Station = Base.classes.station

#session = Session(engine)


app = Flask(__name__)



#Home page.
#List all routes that are available.

@app.route("/")
def home():
    return (
        f"Trip to Hawaii! <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
        filter(Measurement.date >= '2016-08-23').\
        group_by(Measurement.date).all()
    return jsonify(results)

#Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    results2 = session.query(Station.station, Station.name).all()
    return jsonify(results2)


#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    results3 = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
    return jsonify(results3)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<date>")
def start(date):
    results4 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(results4)

@app.route("/api/v1.0/<start>/<end>")
def startDateEnd(start,end):
    results5 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(results5)

if __name__ == "__main__":
    app.run(debug=True)