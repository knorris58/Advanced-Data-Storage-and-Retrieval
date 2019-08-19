import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date/<start_date><br/>"
        f"/api/v1.0/start-date<start_date>/end-date/<end_date>"
    )



@app.route("/api/v1.0/precipitation")
def names():
    """JSON representation of your dictionary"""
    session = Session(engine)
    qry1 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.date >= '2016-08-23').all()

    # Create a dictionary from the row data and append to a list 
    date_prcp = []
    for date, prcp in qry1:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["prcp"] = prcp
        date_prcp.append(date_prcp_dict)

    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def names2():
    """JSON representation of your dictionary"""
    session = Session(engine)
    station_query = session.query(Station.station,Station.name).all()

    stations = []
    for station,name in station_query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        stations.append(station_dict)

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def names3():
    """JSON representation of your dictionary"""
    session = Session(engine)
    temp_observations = session.query(Measurement.date,Measurement.tobs).group_by(Measurement.date).\
    filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').all()


    temperature = []
    for date,tobs in temp_observations:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temperature.append(temp_dict)

    return jsonify(temperature)

@app.route("/api/v1.0/start-date/<start_date>")
def names4(start_date):
    """JSON representation of your dictionary"""
    session = Session(engine)
    start_date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).group_by(Measurement.date).\
        filter(Measurement.date >= start_date).all()


    date = []
    for Min,Avg,Max  in start_date_query:
        date_dict = {}
        date_dict["min"] = Min
        date_dict["avg"] = Avg
        date_dict["max"] = Max        
        date.append(date_dict)

    return jsonify(date)


@app.route("/api/v1.0/start-date<start_date>/end-date/<end_date>")
def names5(start_date,end_date):
    """JSON representation of your dictionary"""
    session = Session(engine)
    start_end_date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).group_by(Measurement.date).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


    date2 = []
    for Min,Avg,Max  in start_end_date_query:
        date_dict2 = {}
        date_dict2["min"] = Min
        date_dict2["avg"] = Avg
        date_dict2["max"] = Max        
        date2.append(date_dict2)

    return jsonify(date2)


if __name__ == '__main__':
    app.run(debug=True)



