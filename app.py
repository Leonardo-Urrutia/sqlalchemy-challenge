from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/lastyearprecipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Observations from most active station: USC00519281:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Format for dates = <strong>&quot;YYYY-MM-DD&quot;</strong><br/>"
        f"Date ranges from <strong>2010-01-01</strong> through <strong>2017-08-23</strong>:<br/>"
        f"/api/v1.0/&#60;start&#62;<br/>"
        f"/api/v1.0/&#60;start&#62;/&#60;end&#62;"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_prcp = []

    for date, prc in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prc
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)


@app.route("/api/v1.0/lastyearprecipitation")
def lastYearPrecipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_prcp = []

    for date, prc in results:
        prcp_dict = {}
        if date >= '2016-08-23' and date <= '2017-08-23':
            prcp_dict["Date"] = date
            prcp_dict["Precipitation"] = prc
            all_prcp.append(prcp_dict)
        
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").all()

    session.close()

    all_tobs = []

    for sta, date, tob in results:
        tobs_dict = {}
        if date >= '2016-08-23' and date <= '2017-08-23':
            tobs_dict["Date"] = date
            tobs_dict["Temp. Observations"] = tob
            all_tobs.append(tobs_dict)
        
    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def startdate(start):
    session = Session(engine)
    results = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        group_by(Measurement.station).\
        filter(Measurement.station == "USC00519281", Measurement.date > start).all()

    session.close()
    start_tobs = list(np.ravel(results))
    return jsonify(start_tobs)    




@app.route("/api/v1.0/<start>/<end>")
def startenddate(start, end):
    session = Session(engine)
    results = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        group_by(Measurement.station).\
        filter(Measurement.station == "USC00519281", Measurement.date >= start, Measurement.date <= end).all()

    session.close()
    start_end_tobs = list(np.ravel(results))
    return jsonify(start_end_tobs)    




if __name__ == '__main__':
    app.run(debug=True)